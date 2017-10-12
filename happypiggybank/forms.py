from django.forms import ModelForm
from django import forms
from django.utils.html import mark_safe
import json
import logging
from . import models


class StoryForm(ModelForm):
    class Meta:
        model = models.Story
        fields = ['message', 'files']
