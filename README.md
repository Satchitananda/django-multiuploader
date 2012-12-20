django-multiuploader
====================

django-multiuploader - is an application which enable ability to upload multiple files with HTML5 (jQuery plugin) in Django.

Installation
============

    $ pip install django-multiuploader

Then you should append 'multiuploader' to your INSTALLED_APPS and run ::

    $ python manage.py syncdb

or, if you use South:

    $ python manage.py migrate multiuploader

Also, if you want previews for uploaded images you need to do syncdb for sorl.thumbnail.

You must have at least Django 1.3.1 version or later.

Also you need to append  'multiuploader.context_processors.booleans' to your ``TEMPLATE_CONTEXT_PROCESSORS``.

Setup
=====

In your settings.py you may use these options to configure application:

* ALLOWED_FILE_TYPES - list of file types, allowed to upload (e.g. ["txt","zip","jpg","jpeg","flv","png"]);
* CONTENT_TYPES - list of content types, allowed to use (e.g. ['image/jpeg', 'video/mp4','application/msword']);
* MAX_UPLOAD_SIZE - maximum size allowed to upload (in bytes)
* MAX_FILE_NUMBER - maximum number of files allowed to upload
* MULTI_FILES_FOLDER - media location where to store files
* FILE_EXPIRATION_TIME - time, when the file is expired (and it can be cleaned with clean_files command).

All this parameters are optional.

Usage
=====

### Uploader form

To upload files you should do a few simple steps:

Append ``urlpattern (r'^your_uploads/', include('multiuploader.urls'))`` to your urlpatterns.
Create MultiUploadForm() in your views and set it to context

Example:

    :::python

        from django.shortcuts import render_to_response
        from multiuploader.forms import MultiUploadForm
        
        def my_view(request):
            context = {
                'uploadForm':MultiUploadForm()
            }
            return render_to_response(your_template, context=context)

Append to your form, where you want upload files MultiuploaderField:

### Example:

    :::python

        # Your forms.py
        
        from multiuploader.forms import MultiuploaderField
        class PostMessageForm(forms.Form):
            text = forms.CharField(label=u'Вопрос', widget=forms.Textarea)
            uploadedFiles = MultiuploaderField(required=False)

Then you should render this field in your template::
    
        <form method="POST" action="" enctype="multipart/form-data">
	    {% csrf_token %}
	    <p>
		    {{ form.text }}
		    {{ form.text.errors }}
		    {{ form.uploadedFiles }}
	    </p>
	    <p>
		    {% multiuploader_noscript form.uploadedFiles.html_name %}
		
		    <input id="send" type="submit" value="Send" class="button">
		    <a id="showUpload" type="button" class="button"><i class="attachment"></i>Attach files</a> 
	    </p>
        </form>
    
    {% multiuploader_form uploadForm form.uploadedFiles.html_name "$" "fileUploads" %}


In this example ``{% multiuploader_noscript form.uploadedFiles.html_name %}`` template tag loads code which shown only for browsers with javascript turned to off.

* ``form.uploadedFiles.html_name`` - argument to template tag defines an element name.

``{% multiuploader_form uploadForm form.uploadedFiles.html_name "fileUploads" %}`` template tag loads code which does all needed logic.
    
* ``uploadForm`` - our multiuploader form
* ``form.uploadedFiles.html_name`` - htrml field name of MultiuploaderField (to store our files)
* ``"$"`` - the jQuery prefix (useful when you want to create multiuploader in admin panel). This parameter is optional
* ``"fileUploads"`` - the name of id (form container) in which you want to create form. Useful for styling.  This parameter is optional.


### Templates

* ``multiuploader/widget.html`` - ``MultiuploaderField`` widget template. Here you can customize look'n'feel of widget.
* ``multiuploader/form.html`` - ``MultiUploadForm`` template.
* ``multiuploader/collectfiles.html`` - JavaScript to collect uploaded file ids
* ``multiuploader/noscript.html`` - template for <noscript> case.

Development
===========

The development is on following the repository:

* https://bitbucket.org/Satchitananda/django-multiuploader


All the feature requests, ideas, bug-reports etc. write in tracker: https://bitbucket.org/Satchitananda/django-multiuploader/issues

Additional appreciation
=======================

* Sebastian Tschan for jQuery HTML5 Uploader (https://blueimp.net/).
* Iurii Garmash for [django multiuploader skeleton](https://github.com/garmoncheg/django_multiuploader),  which was the codebase for this app.


License
=======

Released under the [MIT license](http://www.opensource.org/licenses/MIT).
