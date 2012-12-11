from django import template
from django.conf import settings

register = template.Library()

"""@register.inclusion_tag('multiuploader/collectfiles.html')
def multiuploader_collectfiles(js_prefix = "$", sendButtonId = None, uploadedField = None, lockSendButton = False):
    return {
            'prefix':js_prefix,
            'sendButtonId':sendButtonId,
            'uploadedWidgetHtmlName': uploadedField,
            'lock_submit':lockSendButton
           }"""


@register.inclusion_tag('multiuploader/noscript.html')
def multiuploader_noscript(uploadedField = None):
    return {
            'uploadedWidgetHtmlName': uploadedField
           }

@register.inclusion_tag('multiuploader/form.html')
def multiuploader_form(form,targetformfieldname,js_prefix = "$", sendButtonId = None, elementid="",lock_while_uploading=True):
    return {
            'prefix':js_prefix,
            'sendButtonId': sendButtonId,
            'elementId':elementid,
            'multiuploader_form': form,
            'targetformfieldname':targetformfieldname,
            'lock_while_uploading':lock_while_uploading
           }
