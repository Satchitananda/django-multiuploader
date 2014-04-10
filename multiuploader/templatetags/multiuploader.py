from django import template
from django.conf import settings
from django.core.signing import Signer
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

from .. import default_settings as DEFAULTS
from ..forms import MultiUploadForm

register = template.Library()


@register.simple_tag(takes_context=True)
def form_type(context, form_type):
    mu_forms = getattr(settings, "MULTIUPLOADER_FORMS_SETTINGS", DEFAULTS.MULTIUPLOADER_FORMS_SETTINGS)

    signer = Signer()

    if form_type:
        import warnings

        if form_type == '' or form_type not in mu_forms:
            if settings.DEBUG:
                warnings.warn(
                    "A {% form_type %} was used in a template but such form_type (%s) was not provided in settings, default used instead" % form_type)

            return mark_safe(
                u"<div style='display:none'><input type='hidden' name='form_type' value='%s' /></div>" % signer.sign(
                    'default'))

        else:
            return mark_safe(
                u"<div style='display:none'><input type='hidden' name='form_type' value='%s' /></div>" % signer.sign(
                    form_type))
    else:
        # It's very probable that the form_type is missing because of
        # misconfiguration, so we raise a warning

        if settings.DEBUG:
            warnings.warn("A {% form_type %} was used in a template but form_type was not provided")

        return mark_safe(u"")


@register.simple_tag(takes_context=True)
def multiuploader_form(context, form_type="default", extended_rights=False, template="multiuploader/form.html", target_form_fieldname=None,
                       js_prefix="jQuery", send_button_selector=None,
                       wrapper_element_id="", lock_while_uploading=True, number_files_attached=0):
    return render_to_string(template, {
        'multiuploader_form': MultiUploadForm(form_type=form_type, extended_rights=extended_rights),
        'csrf_token': context["csrf_token"],
        'type': form_type,
        'prefix': js_prefix,
        'send_button_selector': send_button_selector,
        'wrapper_element_id': wrapper_element_id,
        'target_form_fieldname': target_form_fieldname,
        'lock_while_uploading': lock_while_uploading,
        'number_files_attached': number_files_attached
    })


@register.inclusion_tag('multiuploader/noscript.html')
def multiuploader_noscript(uploaded_field=None):
    return {
        'uploaded_widget_html_name': uploaded_field
    }