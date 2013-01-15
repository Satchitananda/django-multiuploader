import os
import magic

from django import forms
from django.utils import simplejson
from django.utils.html import mark_safe
from django.conf import settings,Settings
from django.template.loader import render_to_string
from django.core.validators import validate_integer
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

from utils import format_file_extensions

from multiuploader import DEFAULTS

class MultiuploadWidget(forms.MultipleHiddenInput):
    def __init__(self, attrs={}):
        super(MultiuploadWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        widget_ = super(MultiuploadWidget, self).render(name, value, attrs)
        output = '<div id="hidden_container" style="display:none;">%s</div>'%widget_
        return mark_safe(output)

class MultiuploaderField(forms.MultiValueField):
    widget = MultiuploadWidget()

    def formfield(self, **kwargs):
        kwargs['widget'] = MultiuploadWidget
        return super(MultiuploaderField, self).formfield(**kwargs)

    def validate(self,values):
        super(MultiuploaderField,self).validate(values)

    def clean(self, values):
        super(MultiuploaderField,self).clean(values)
        return values

    def compress(self,value):
        if value!=None:
            return [i for i in value]

class MultiUploadForm(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        settings_max_file_size = getattr(settings,"MULTIUPLOADER_MAX_FILE_SIZE", DEFAULTS.MULTIUPLOADER_MAX_FILE_SIZE)
        settings_file_types = format_file_extensions(getattr(settings,"MULTIUPLOADER_ALLOWED_FILE_TYPES", DEFAULTS.MULTIUPLOADER_ALLOWED_FILE_TYPES))
        settings_max_file_number = getattr(settings,"MULTIUPLOADER_MAX_FILE_NUMBER",DEFAULTS.MULTIUPLOADER_MAX_FILE_NUMBER)

        defaults = {
            'maxFileSize': settings_max_file_size,
            'acceptFileTypes': settings_file_types,
            'maxNumberOfFiles': settings_max_file_number,
        }

        options = {}

        if "options" in kwargs and kwargs["options"] !={} and kwargs["options"] is not None:
            options = kwargs["options"]

        for key in defaults.keys():
            if not key in options:
                options[key] = defaults[key]

        self.options = simplejson.dumps(options)

        super(MultiUploadForm, self).__init__(*args,**kwargs)

        self.fields["file"].widget=forms.FileInput(attrs={ 'multiple': True })

    def clean_file(self):
        content = self.cleaned_data[u'file']
        allowed_content_types = getattr(settings, "MULTIUPLOADER_CONTENT_TYPES",DEFAULTS.MULTIUPLOADER_CONTENT_TYPES)
        max_file_size = getattr(settings,"MULTIUPLOADER_MAX_FILE_SIZE",DEFAULTS.MULTIUPLOADER_MAX_FILE_SIZE)
        allowed_file_extensions = getattr(settings, "MULTIUPLOADER_ALLOWED_FILE_TYPES",DEFAULTS.MULTIUPLOADER_ALLOWED_FILE_TYPES)

        filename, extension = os.path.splitext(content.name)
        extension = extension.replace(".","")

        #Checking fileextension, content-type and file size
        if extension not in allowed_file_extensions:
            raise forms.ValidationError(_('File type is not supported'))

        content_type = magic.from_buffer(content.read(1024), mime=True)

        if content_type in allowed_content_types:
            if content._size > max_file_size:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(max_file_size), filesizeformat(content._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))

        return content