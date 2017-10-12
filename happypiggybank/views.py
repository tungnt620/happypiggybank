# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
import os
from django.core.urlresolvers import reverse
from django.db import connection

from common import string_utils
from root import settings
from . import forms
from . import models
from django.views.generic import View


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class AddStoryView(View):
    template_name = 'view_story.html'
    form_class = forms.StoryForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        files = request.FILES.getlist('files')
        if form.is_valid():
            file_names = handle_upload_files(files)
            form.instance.message = form.instance.message.strip()
            form.instance.files = file_names
            form.save()

        return render(request, self.template_name, {'story': form.instance})


def handle_upload_files(upload_files):
    file_names = []
    for upload_file in upload_files:
        file_name = handle_uploaded_file(upload_file)
        file_names.append(file_name)
    return "|".join(file_names)

def handle_uploaded_file(upload_file):
    file_name = string_utils.random_string(10) + upload_file.name
    fpath = os.path.join(settings.MEDIA_ROOT, file_name)
    with open(fpath, 'wb+') as destination:
        for chunk in upload_file.chunks():
            destination.write(chunk)
    return file_name


class ViewStoryView(View):
    template_name = 'view_story.html'

    def get(self, request, *args, **kwargs):
        story_id = kwargs['story_id']
        story = models.Story.objects.filter(id=story_id).first()
        story.read_times = story.read_times + 1
        story.save()
        return render(request, self.template_name, {'story': story})


class PickStoryView(View):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""SELECT id FROM story  
                              ORDER BY RANDOM() LIMIT 1""")
            data = cursor.fetchall()
            if data:
                story_id = data[0][0]
                return HttpResponseRedirect(reverse('view_story', kwargs={'story_id': story_id}))
            else:
                return render(request, 'home.html', {'err_message': u"Hiện tại heo đất chưa có câu chuyện nào về các bạn!"})
