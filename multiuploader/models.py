import os

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from multiuploader.utils import generate_safe_pk, _upload_to


class BaseAttachment(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    filename = models.CharField(max_length=255, blank=False, null=False)
    upload_date = models.DateTimeField()

    @generate_safe_pk
    def generate_pk(self):
        return self

    def save(self, *args, **kwargs):
        if not self.upload_date:
            self.upload_date = now()

        if not self.pk:
            self.pk = self.generate_pk()

        super(BaseAttachment, self).save(*args, **kwargs)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s' % self.filename


class MultiuploaderFile(BaseAttachment):
    file = models.FileField(upload_to=_upload_to, max_length=255)

    def save(self, *args, **kwargs):
        self.filename = os.path.basename(self.file.path)
        return super(MultiuploaderFile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('multiuploader file')
        verbose_name_plural = _('multiuploader files')
