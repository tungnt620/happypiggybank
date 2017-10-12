# -*- coding: utf-8 -*-
import os

from django.core.management.base import BaseCommand
from root import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.replace_project_name()

    def replace_project_name(self):
        project_name = raw_input('Enter project name: ')
        if not project_name:
            return
        # ELSE
        for root, dirs, files in os.walk(settings.BASE_DIR):
            if '.git' in root:
                continue
            for filename in files:
                fpath = os.path.join(root, filename)
                print fpath
                if not os.path.isfile(fpath):
                    continue
                # ELSE
                lines = []
                with open(fpath) as infile:
                    for line in infile:
                        line = line.replace('{{'+'project_name'+'}}', project_name)
                        lines.append(line)
                with open(fpath, 'w') as outfile:
                    for line in lines:
                        outfile.write(line)

                # Rename file
                if filename.startswith("project_name"):
                    new_filename = filename.replace('project_name', project_name)
                    os.rename(fpath, os.path.join(root, new_filename))
