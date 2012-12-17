import os
import logging
import datetime

from shutil import move
from datetime import timedelta
from django.core.files import File
from models import MultiuploaderFile
from django.conf import settings,Settings
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile

log = logging

DEFAULTS =  Settings("multiuploader.default_settings")


#Getting files here
def formatFileExtensions(extensions):
    return  "/.(%s)$/i" % "|".join(extensions)

def get_uploads_from_request(request):
    """Description should be here"""
    attachments = []
    #We're only supports POST
    if request.method == 'POST':
        if request.FILES == None:
            return []

        #getting file data for further manipulations
        if not u'files' in request.FILES:
            return []
        
        for fl in request.FILES.getlist("files"):
            wrapped_file = UploadedFile(fl)
            filename = wrapped_file.name
            #Need a bit later to calculate all file count
            file_size = wrapped_file.file.size
            attachments.append({"file":fl,"date":datetime.datetime.now(),"name":wrapped_file.name})
        
    return attachments

def get_uploads_from_temp(ids):
    """Method returns of uploaded files"""
    #from django.db.models.fields.files.FieldFile 
    ats = []
    files = MultiuploaderFile.objects.filter(id__in=ids)
    
    #Getting THE FILES
    for fl in files:
        ats.append({"file":File(fl.file),"date":fl.upload_date,"name":fl.filename})
        
    return ats

def get_uploads_from_model(fromModelEntity,filesAttrName):
    """Replaces attachment files from model to a given location, 
       returns list of opened files of dict {file:'file',date:date,name:'filename'}"""
    
    ats = []
    files = getattr(fromModelEntity,filesAttrName)

    for fl in files:
        ats.append({"file":File(fl.file),"date":fl.upload_date,"name":fl.filename})
            
    return ats

def cleanAttachments(print_to_console=False):
    expiration_time = getattr(settings,"EXPIRATION_TIME",DEFAULTS.EXPIRATION_TIME)
    time_threshold = datetime.datetime.now() - timedelta(seconds=expiration_time)
    
    for attach in MultiuploaderFile.objects.filter(upload_date__lt=time_threshold):
        filepath = os.path.join(settings.MEDIA_ROOT,attach.file.name)      
        try:
            os.remove(filepath)
        except Exception as e:
            if print_to_console:
                print e

    MultiuploaderFile.objects.all().delete()
    
    if print_to_console:
        print "Cleaning temporary upload files complete"
