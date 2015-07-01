from django import forms
from multiuploader.forms import MultiuploaderField

class TargetForm(forms.Form):
    uploaded_files = MultiuploaderField(required=False)
    deleted_files = MultiuploaderField(required=False)
