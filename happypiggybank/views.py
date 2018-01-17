# -*- coding: utf-8 -*-

import json

from django.shortcuts import render, redirect
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.db import connection
from django.core.cache import cache
from django.views.generic import View, TemplateView

from common import file_utils
from common import string_utils
from happypiggybank import forms
from happypiggybank import models
from happypiggybank import constants


class BaseView(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        return super(BaseView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context['group'] = self.get_hpb_group(self.request)
        return context

    def get_hpb_group(self, request):
        group = models.UserHPBGroup.objects.filter(user_id=request.user.pk).first()
        if not group:
            group = models.HPBGroup.objects.create()
            models.UserHPBGroup.objects.create(user_id=request.user.pk,
                                               hpb_group_id=group.pk)
        return group


class AuthView(BaseView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(BaseView, self).dispatch(request, *args, **kwargs)


class HomeView(BaseView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class AddStoryView(AuthView):
    template_name = 'view_story.html'
    form_class = forms.StoryForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        files = request.FILES.getlist('files')
        context = self.get_context_data(**kwargs)
        if form.is_valid():
            file_names = file_utils.handle_upload_files(files)
            form.instance.files = file_names
            form.instance.hpb_group_id = context['group'].pk
            form.save()

        story_temp_id = string_utils.random_string(size=15)
        cache.set(story_temp_id, form.instance.id, constants.CACHE_STORY_SLUG_RANDOM_TIME)
        return HttpResponseRedirect(reverse('view_story', kwargs={'story_temp_id': story_temp_id}))


class ViewStoryView(AuthView):
    template_name = 'view_story.html'

    def get(self, request, *args, **kwargs):
        story_temp_id = kwargs['story_temp_id']
        story_id = cache.get(story_temp_id, None)
        if not story_id:
            return HttpResponseRedirect(reverse('home'))

        story = models.Story.objects.filter(id=story_id).first()
        story.read_times = story.read_times + 1
        story.save()
        return render(request, self.template_name, {'story': story})


class PickStoryView(AuthView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        with connection.cursor() as cursor:
            # For sqlite, if switch to other database need change syntax
            cursor.execute("""SELECT id FROM story WHERE hpb_group_id = %s
                              ORDER BY RANDOM() LIMIT 1""" % context['group'].pk)
            data = cursor.fetchall()
            if data:
                story_id = data[0][0]
                story_temp_id = string_utils.random_string(size=15)
                cache.set(story_temp_id, story_id, constants.CACHE_STORY_SLUG_RANDOM_TIME)

                return HttpResponseRedirect(reverse('view_story', kwargs={'story_temp_id': story_temp_id}))
            else:
                return render(request, 'home.html', {'err_message': u"Hiện tại heo đất chưa có câu chuyện nào về các bạn!"})


class StoryCommentView(AuthView):

    def post(self, request, *args, **kwargs):
        section_id =request.POST.get('sectionId', '')
        comment = request.POST.get('comment', '')

        models.StoryComment.objects.create(section_id=section_id,
                                           comment=comment,
                                           user_id=request.user.pk)

        return HttpResponse(json.dumps(request.POST), content_type="application/json")
