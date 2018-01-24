# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.utils import timezone

from root import settings
from django.db import models


class CreateUpdateModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HPBGroup(CreateUpdateModel):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return str(self.pk)

    def to_dict(self):
        return {'id': self.id, 'name': self.name}

    class Meta:
        db_table = 'hpb_group'


class UserHPBGroup(CreateUpdateModel):
    user_id = models.BigIntegerField(db_index=True)
    hpb_group_id = models.BigIntegerField(db_index=True)

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        db_table = 'user_hpb_group'


class Story(CreateUpdateModel):
    message = models.TextField(default='', blank=True)
    files = models.TextField(null=True, blank=True)
    read_times = models.PositiveSmallIntegerField(default=0)
    user_id = models.BigIntegerField(db_index=True)
    hpb_group_id = models.BigIntegerField(default=0, db_index=True)

    def list_file_meta_data(self):
        file_names = self.files.split('|')
        file_meta_data = []
        for file_name in file_names:
            relative_file_url = os.path.join(settings.MEDIA_URL, file_name)
            if file_name[-3:].lower() in settings.IMAGE_EXTENSION:
                type = 'image'
            else:
                type = 'video'
            file_meta_data.append( (type, relative_file_url))
        return file_meta_data

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        db_table = 'story'


class StoryComment(CreateUpdateModel):
    section = models.CharField(max_length=255)
    comment = models.TextField(null=True, blank=True)
    user_id = models.BigIntegerField(null=False)

    def __unicode__(self):
        return str(self.comment)

    class Meta:
        db_table = 'story_comment'