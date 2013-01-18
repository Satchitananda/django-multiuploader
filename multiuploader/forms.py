import os
import magic

from django import forms
from django.conf import settings
from django.utils import simplejson
from django.utils.html import mark_safe
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
        settings_max_file_size = getattr(settings, "MULTIUPLOADER_MAX_FILE_SIZE", DEFAULTS.MULTIUPLOADER_MAX_FILE_SIZE)
        settings_file_types = format_file_extensions(getattr(settings,"MULTIUPLOADER_ALLOWED_FILE_TYPES", DEFAULTS.MULTIUPLOADER_ALLOWED_FILE_TYPES))
        settings_max_file_number = getattr(settings, "MULTIUPLOADER_MAX_FILE_NUMBER", DEFAULTS.MULTIUPLOADER_MAX_FILE_NUMBER)
        settings_allowed_content_types = getattr(settings, "MULTIUPLOADER_CONTENT_TYPES", DEFAULTS.MULTIUPLOADER_CONTENT_TYPES)

        options = {
            'maxFileSize': settings_max_file_size,
            'acceptFileTypes': settings_file_types,
            'maxNumberOfFiles': settings_max_file_number,
            'allowedContentTypes': settings_allowed_content_types
        }

        user_options = kwargs.pop("options",{})
        options.update(user_options)

        self.options = simplejson.dumps(options)
        self._options = options

        super(MultiUploadForm, self).__init__(*args,**kwargs)

        self.fields["file"].widget=forms.FileInput(attrs={ 'multiple': True })

    def clean_file(self):
        content = self.cleaned_data[u'file']

        allowed_content_types = self._options["allowedContentTypes"]
        max_file_size = self._options["maxFileSize"]
        allowed_file_extensions = self._options["acceptFileTypes"]

        filename, extension = os.path.splitext(content.name)
        extension = extension.replace(".","")

        #Checking fileextension, content-type and file size
        if extension not in allowed_file_extensions:
            raise forms.ValidationError("acceptFileTypes")
            #raise forms.ValidationError(_('File type is not supported'))

        content_type = magic.from_buffer(content.read(1024), mime=True)

        if content_type in allowed_content_types:
            if content._size > max_file_size:
                raise forms.ValidationError("maxFileSize")
                #raise forms.ValidationError(_('Please keep filesize under %(max_file_size)s. Current file size %(filesize)s') % {'max_file_size' : filesizeformat(max_file_size), 'filesize' : filesizeformat(content._size)})
        else:
            raise forms.ValidationError("acceptFileTypes")
            #raise forms.ValidationError(_('File type is not supported'))

        return content