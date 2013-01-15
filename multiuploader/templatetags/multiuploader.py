from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('multiuploader/noscript.html')
def multiuploader_noscript(uploaded_field = None):
    return {
            'uploaded_widget_html_name': uploaded_field
           }

@register.inclusion_tag('multiuploader/form.html')
def multiuploader_form(form, target_form_fieldname, js_prefix = "$", send_button_selector = None, wrapper_element_id = "", lock_while_uploading = True):
    return {
            'prefix': js_prefix,
            'send_button_selector': send_button_selector,
            'wrapper_element_id': wrapper_element_id,
            'multiuploader_form': form,
            'target_form_fieldname': target_form_fieldname,
            'lock_while_uploading': lock_while_uploading
           }
