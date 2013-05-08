django-multiuploader
====================

django-multiuploader - is an application which enable ability to upload
multiple files with HTML5 (jQuery plugin) in Django.

Installation
============

::

    $ pip install django-multiuploader

Then you should append ‘multiuploader’ to your INSTALLED\_APPS and run

::

    $ python manage.py syncdb

or, if you use South:

::

    $ python manage.py migrate multiuploader

Also, if you want previews for uploaded images you need to do syncdb for
sorl.thumbnail.

You must have at least Django 1.3.1 version or later.

Also you need to append ‘multiuploader.context\_processors.booleans’ to
your ``TEMPLATE_CONTEXT_PROCESSORS``.

Setup
=====

In your settings.py you may use these options to configure application:

``MULTIUPLOADER_FILES_FOLDER`` = 'multiuploader' - media location where to store files

``MULTIUPLOADER_FILE_EXPIRATION_TIME`` = 3600 - time, when the file is expired (and it can be cleaned with clean\_files command).

``MULTIUPLOADER_FORMS_SETTINGS`` = 
:: 

    {
    'default': {
        'FILE_TYPES' : ["txt","zip","jpg","jpeg","flv","png"],
        'CONTENT_TYPES' : [
                'image/jpeg',
                'image/png',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/vnd.ms-powerpoint',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'application/vnd.oasis.opendocument.text',
                'application/vnd.oasis.opendocument.spreadsheet',
                'application/vnd.oasis.opendocument.presentation',
                'text/plain',
                'text/rtf',
                    ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER':5,
	'AUTO_UPLOAD': True,
    },
    'images':{
        'FILE_TYPES' : ['jpg', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'tiff', 'ico' ],
        'CONTENT_TYPES' : [
            'image/gif',
            'image/jpeg',
            'image/pjpeg',
            'image/png',
            'image/svg+xml',
            'image/tiff',
            'image/vnd.microsoft.icon',
            'image/vnd.wap.wbmp',
            ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER':5,
	'AUTO_UPLOAD': True,
    },
    'video':{
        'FILE_TYPES' : ['flv', 'mpg', 'mpeg', 'mp4' ,'avi', 'mkv', 'ogg', 'wmv', 'mov', 'webm' ],
        'CONTENT_TYPES' : [
            'video/mpeg',
            'video/mp4',
            'video/ogg',
            'video/quicktime',
            'video/webm',
            'video/x-ms-wmv',
            'video/x-flv',
            ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER':5,
	'AUTO_UPLOAD': True,
    },
    'audio':{
        'FILE_TYPES' : ['mp3', 'mp4', 'ogg', 'wma', 'wax', 'wav', 'webm' ],
        'CONTENT_TYPES' : [
            'audio/basic',
            'audio/L24',
            'audio/mp4',
            'audio/mpeg',
            'audio/ogg',
            'audio/vorbis',
            'audio/x-ms-wma',
            'audio/x-ms-wax',
            'audio/vnd.rn-realaudio',
            'audio/vnd.wave',
            'audio/webm'
            ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER':5,
	'AUTO_UPLOAD': True,
    }} 
    

it is a dictionary with multiple form settings. When you append a multiuploader, you can choose a preconfigured form type, which will accept only extensions and content types you've provided.


All these parameters are optional.

Usage
=====

Uploader form
~~~~~~~~~~~~~

To upload files you should do a few simple steps:

Append ``urlpattern (r'^your_uploads/', include('multiuploader.urls'))``
to your urlpatterns. Create MultiUploadForm() in your views and set it
to context

Example:

::

        from django.shortcuts import render_to_response
        from multiuploader.forms import MultiUploadForm

        def my_view(request):
            context = {
                'uploadForm':MultiUploadForm()
            }
            return render_to_response(your_template, context=context)

Append to your form, where you want upload files MultiuploaderField:

Example:
~~~~~~~~

::

    # Your forms.py

    from multiuploader.forms import MultiuploaderField
    class PostMessageForm(forms.Form):
        text = forms.CharField(label=u'Question', widget=forms.Textarea)
        uploadedFiles = MultiuploaderField(required=False)

Then you should render this field in your template::

        {% load multiuploader %}
        
        <form method="POST" action="" enctype="multipart/form-data">
        {% csrf_token %}
        <p>
            {{ form.text }}
            {{ form.text.errors }}
            {{ form.uploadedFiles }} {{ form.uploadedFiles.errors }}
        </p>
        <p>
            {% multiuploader_noscript form.uploadedFiles.html_name %}

            <input id="send" type="submit" value="Send" class="button">
            <a id="showUpload" type="button" class="button"><i class="attachment"></i>Attach files</a> 
        </p>
        </form>

        {% multiuploader_form form_type="default" template="multiuploader/form.html" target_form_fieldname=forms.edit.uploadedFiles.html_name js_prefix="jQuery" send_button_selector="input[name=_edit]" wrapper_element_id="fileUploads" lock_while_uploading=True number_files_attached=forms.attached_count %}

In this example

``{% multiuploader_noscript form.uploadedFiles.html_name %}`` template tag loads code which shown only for browsers with javascript turned to off.

-  ``form.uploadedFiles.html_name`` - argument to template tag defines
   an element name.

``{% multiuploader_form form_type="default" template="multiuploader/form.html" target_form_fieldname=forms.edit.uploadedFiles.html_name js_prefix="jQuery" send_button_selector="input[name=_edit]" wrapper_element_id="fileUploads" lock_while_uploading=True number_files_attached=forms.attached_count %}`` template tag loads code which does all needed logic.

-  ``form_type`` - type of form with predefined settings, defined in your settings.py in MULTIUPLOADER_FORMS_SETTINGS dictionary
-  ``template`` - template for multiuploader
-  ``target_form_fieldname`` - html field name of MultiuploaderField in our case it's a name of uploadedFiles
-  ``js_prefix`` - the jQuery prefix (useful when you want to create multiuploader in admin panel). This parameter is optional
-  ``send_button_selector`` - jQuery selector for field we should lock, while file uploading
-  ``wrapper_element_id`` - the name of id (form container) in which you want to create form. Useful for styling. This parameter is optional
-  ``lock_while_uploading`` is a boolean variable which controlls whether multiuploader should lock submit while uploading or not. This parameter is optional

These parameters may used as positional too.

Templates
~~~~~~~~~

-  ``multiuploader/form.html`` - ``MultiUploadForm`` template, you can change look'n'feel here.
-  ``multiuploader/noscript.html`` - template for noscript case.

Development
===========

The development is on following the repository:

-  https://bitbucket.org/Satchitananda/django-multiuploader

All the feature requests, ideas, bug-reports etc. write in tracker:
-  https://bitbucket.org/Satchitananda/django-multiuploader/issues

Additional appreciation
=======================

-  Sebastian Tschan for jQuery HTML5 Uploader (https://blueimp.net/).
-  Iurii Garmash for `django multiuploader skeleton`_, which was the
   codebase for this app.

License
=======

Released under the `MIT license`_.

.. _django multiuploader skeleton: https://github.com/garmoncheg/django_multiuploader
.. _MIT license: http://www.opensource.org/licenses/MIT
