import os
import time
import datetime
from hashlib import sha1
from django.db import models
from django.conf import settings
from django.utils.text import get_valid_filename
from django.core.files.storage import default_storage
from django.utils.encoding import force_unicode, smart_str

def get_filename(upload_to, storage=default_storage):
    def _filename(instance, filename):
        filename = get_valid_filename(filename)
        filename, ext = os.path.splitext(filename)
        hash = sha1(str(time.time())).hexdigest()
        fullname = os.path.join(upload_to,"%s.%s%s" %(filename,hash,ext)) #storage.get_available_name(os.path.join(upload_to, filename))
        return fullname
    return _filename

upload_to = getattr(settings, 'MULTI_FILES_FOLDER', 'attachments') + '/'

class MultiuploaderFile(models.Model):
    """Model for storing uploaded files"""
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_filename(upload_to=upload_to), max_length=255)
    upload_date = models.DateTimeField(default=datetime.datetime.now())