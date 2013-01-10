import os
import time
import datetime

from hashlib import sha1
from random import choice

from django.db import models
from django.conf import settings
from django.utils.text import get_valid_filename
from django.core.files.storage import default_storage
from django.utils.encoding import force_unicode, smart_str

from multiuploader import DEFAULTS

class Attachment(models.Model):
    FILE_UPLOAD_PATH = 'attachments'

    id = models.CharField(primary_key=True, max_length=255)
    filename = models.CharField(max_length=255, blank=False, null=False)
    file = models.FileField(upload_to=FILE_UPLOAD_PATH, max_length=255)
    upload_date = models.DateTimeField(default=datetime.datetime.now())

    def generate_pk(self):
        while 1:
            pk = sha1('%s%s%s' % (settings.SECRET_KEY, self.filename, ''.join([choice('0123456789') for i in range(11)]))).hexdigest()

            try:
                self.__class__.objects.get(pk=pk)
            except:
                return pk

    def save(self, *args, **kwargs):
        if not self.upload_date:
            self.upload_date = datetime.datetime.now()

        if not self.pk:
            self.pk = self.generate_pk()

        super(Attachment, self).save(*args, **kwargs)

    class Meta:
        abstract = True


def get_filename(upload_to, storage=default_storage):
    def _filename(instance, filename):
        filename = get_valid_filename(filename)
        filename, ext = os.path.splitext(filename)
        hash = sha1(str(time.time())).hexdigest()
        fullname = os.path.join(upload_to,"%s.%s%s" % (filename, hash, ext))
        return fullname
    return _filename

upload_to = getattr(settings, 'MULTI_FILES_FOLDER', DEFAULTS.MULTI_FILES_FOLDER) + '/'

class MultiuploaderFile(Attachment):
    FILE_UPLOAD_PATH = get_filename(upload_to=upload_to)


'''    """Model for storing uploaded files"""
    id = models.CharField(primary_key=True, max_length=255)
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_filename(upload_to=upload_to), max_length=255)
    upload_date = models.DateTimeField()
    
    def generate_pk(self):
        while 1:
            pk = sha1('%s%s%s' % (settings.SECRET_KEY, self.filename, ''.join([choice('0123456789') for i in range(11)]))).hexdigest()
           
            try:
                self.__class__.objects.get(pk=pk)
            except:
                return pk
    
    def save(self, *args, **kwargs):
        if not self.upload_date:
            self.upload_date = datetime.datetime.now()
        
        if not self.pk:
            self.pk = self.generate_pk()
        
        super(MultiuploaderFile, self).save(*args, **kwargs)'''
