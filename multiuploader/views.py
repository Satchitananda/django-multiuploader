from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest,HttpResponseServerError
from models import MultiuploaderFile
from django.core.files.uploadedfile import UploadedFile

#importing json parser to generate jQuery plugin friendly json response
from django.utils import simplejson
from django.core.urlresolvers import reverse

#for generating thumbnails
#sorl-thumbnails must be installed and properly configured
from sorl.thumbnail import get_thumbnail
from django.shortcuts import redirect

from forms import MultiUploadForm


import logging
log = logging


def delete_file(pk):
    fl= get_object_or_404(MultiuploaderFile, pk=pk)
    fl.delete()
    log.info('DONE. Deleted photo id='+str(pk))
    

def multiuploader_delete(request, pk):
    """
    View for deleting photos with multiuploader AJAX plugin.
    made from api on:
    https://github.com/blueimp/jQuery-File-Upload
    """
    
    if request.method == 'POST':
        log.info('Called delete file. File id='+str(pk))
        fl= get_object_or_404(MultiuploaderFile, pk=pk)
        fl.delete()
        log.info('DONE. Deleted file id='+str(pk))
        return HttpResponse(str(pk))
    else:
        log.info('Received not POST request to delete file view')
        return HttpResponseBadRequest('Only POST accepted')

def multiuploader(request,noajax=False):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """
    
    if request.method == 'POST':
        log.info('received POST to main multiuploader view')
        
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')
        
        #if not u'files' in request.FILES:
        #    return redirect(request.META['HTTP_REFERER']) 
        
        form = MultiUploadForm(request.POST, request.FILES)

        if not form.is_valid():
            return HttpResponseBadRequest('maxFileSize')
        
        #Now we sure, that our files is not bigger than given size
        
        file = request.FILES[u'file']
        
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        
        log.info ('Got file: "%s"' % str(filename))

        #writing file manually into model
        #because we don't need form of any type.
        
        fl = MultiuploaderFile()
        fl.filename=str(filename)
        fl.file=file
        fl.save()
        
        log.info('File saving done')

        thumb_url = ""
        try:
            im = get_thumbnail(fl.file, "80x80", quality=50)
            thumb_url = im.url
        except Exception as e:
            log.error(e)
            
        #generating json response array
        result = []
        
        result.append({"id":fl.id,
                       "name":filename, 
                       "size":file_size, 
                       "url":reverse('multi-file-link',args=[fl.pk]),
                       "thumbnail_url":thumb_url,
                       "delete_url":reverse('multi-delete',args=[fl.pk]),  
                       "delete_type":"POST",})
        
        response_data = simplejson.dumps(result)
        
        #checking for json data type
        #big thanks to Guy Shapiro
        
        if noajax:
            if request.META['HTTP_REFERER']:
                redirect(request.META['HTTP_REFERER'])
        
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else: #GET
        return HttpResponse('Only POST accepted')


def multi_show_uploaded(request, pk):
    fl = get_object_or_404(MultiuploaderFile, id=pk)
    url = settings.MEDIA_URL+fl.file.name
    return redirect(url)
