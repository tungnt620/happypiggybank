import os
from root import settings
from . import string_utils


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
