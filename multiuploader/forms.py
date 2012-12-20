import os

from django import forms
from django.utils.html import mark_safe
from django.conf import settings,Settings
from django.template.loader import render_to_string
from django.core.validators import validate_integer
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

from utils import format_file_extensions


DEFAULTS =  Settings("multiuploader.default_settings")

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

class MultiUploadFormWidget(forms.FileInput):
    template = 'multiuploader/widget.html'
    
    def __init__(self, prefix="$",attrs={}):
        self.prefix = prefix
        
        if not "multiple" in attrs:
            attrs["multiple"] = True
            
        super(MultiUploadFormWidget, self).__init__(attrs)
        
       
    def render(self, name, value, attrs=None):
        max_usize = getattr(settings,"MAX_FILE_SIZE",DEFAULTS.MAX_FILE_SIZE)
        filetypes = format_file_extensions(getattr(settings,"ALLOWED_FILE_TYPES",DEFAULTS.ALLOWED_FILE_TYPES))
        
        
        maxFileNumber = getattr(settings,"MAX_FILE_NUMBER",DEFAULTS.MAX_FILE_NUMBER) 
        
        widget_ = super(MultiUploadFormWidget, self).render(name, value, attrs)
        output = render_to_string(self.template, {
                                                  'field': widget_,
                                                  'field_name':name,
                                                  'maxFileSize':max_usize,
                                                  'fileTypes': filetypes,
                                                  'maxFileNumber':maxFileNumber,
                                                  'prefix':self.prefix
                                                 })

        return mark_safe(output)
        
class MultiUploadForm(forms.Form):
    file = forms.FileField()
    
    def __init__(self,*args,**kwargs):
        prefix = "$"
        
        if "prefix" in kwargs and kwargs["prefix"] != "":
            prefix = kwargs["prefix"]
            kwargs.pop("prefix")
        
        super(MultiUploadForm, self).__init__(*args,**kwargs)
        self.fields["file"].widget=MultiUploadFormWidget(prefix=prefix)

        
    def clean_file(self):
        content = self.cleaned_data[u'file']
        
        ctypes = getattr(settings, "CONTENT_TYPES",DEFAULTS.CONTENT_TYPES)
        max_usize = getattr(settings,"MAX_FILE_SIZE",DEFAULTS.MAX_FILE_SIZE)
        exts = getattr(settings, "ALLOWED_FILE_TYPES",DEFAULTS.ALLOWED_FILE_TYPES)
        
        filename, extension = os.path.splitext(content.name)
        extension = extension.replace(".","")
        
        #Checking fileextension, content-type and file size
        if extension not in exts:
            raise forms.ValidationError(_('File type is not supported'))
        
        if content.content_type in ctypes:
            if content._size > max_usize:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(max_usize), filesizeformat(content._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))
        
        return content
    
