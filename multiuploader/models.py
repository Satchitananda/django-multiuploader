import os
import time
import datetime

from hashlib import sha1

from django.db import models
from django.conf import settings
from django.utils.text import get_valid_filename
from django.core.files.storage import default_storage

from multiuploader import DEFAULTS
from multiuploader.utils import generate_safe_pk

models.options.DEFAULT_NAMES += ('upload_path', 'make_filename_safe')

def get_filename(storage=default_storage):
    def _filename(instance, filename):
        make_filename_safe = instance._meta.make_filename_safe
        upload_path = instance._meta.upload_path

        if upload_path[-1] != '/':
            upload_path += '/'

        if make_filename_safe:
            filename = get_valid_filename(os.path.basename(filename))
            filename, ext = os.path.splitext(filename)
            hash = sha1(str(time.time())).hexdigest()
            fullname = os.path.join(upload_path, "%s.%s%s" % (filename, hash, ext))
        else:
            filename = get_valid_filename(os.path.basename(filename))
            fullname = os.path.join(upload_path, filename)

        return fullname

    return _filename

class BaseAttachment(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    filename = models.CharField(max_length=255, blank=False, null=False)

    file = models.FileField(upload_to=get_filename(), max_length=255)
    upload_date = models.DateTimeField(default=datetime.datetime.now())

    @generate_safe_pk
    def generate_pk(self):
        return self

    def save(self, *args, **kwargs):
        if not self.upload_date:
            self.upload_date = datetime.datetime.now()

        if not self.pk:
            self.pk = self.generate_pk()

        super(BaseAttachment, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        make_filename_safe = True
        upload_path = getattr(settings, 'MULTIUPLOADER_FILES_FOLDER', DEFAULTS.MULTIUPLOADER_FILES_FOLDER)

class MultiuploaderFile(BaseAttachment):
    pass