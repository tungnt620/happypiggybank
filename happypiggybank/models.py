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


class Story(CreateUpdateModel):
    message = models.TextField(default='', blank=True)
    files = models.TextField(null=True, blank=True)
    read_times = models.PositiveSmallIntegerField(default=0)

    def list_file_meta_data(self):
        file_names = self.files.split('|')
        file_meta_data = []
        for file_name in file_names:
            relative_file_url = os.path.join(settings.MEDIA_URL, file_name)
            if file_name[-3:] in settings.IMAGE_EXTENSION:
                type = 'image'
            else:
                type = 'video'
            file_meta_data.append( (type, relative_file_url))
        return file_meta_data

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        db_table = 'story'
