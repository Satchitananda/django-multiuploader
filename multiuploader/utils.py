import os
import logging
import datetime

from shutil import move
from hashlib import sha1
from random import choice
from datetime import timedelta

from django.core.files import File
from django.conf import settings,Settings
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile

from multiuploader import DEFAULTS
from models import MultiuploaderFile

log = logging


#Getting files here
def format_file_extensions(extensions):
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
    files = MultiuploaderFile.objects.filter(pk__in=ids)
    
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

def generate_safe_pk(self):
    def wrapped(self):
        while 1:
            skey = getattr(settings,'SECRET_KEY','asidasdas3sfvsanfja242aako;dfhdasd&asdasi&du7')
	    pk = sha1('%s%s' % (skey, ''.join([choice('0123456789') for i in range(11)]))).hexdigest()
           
            try:
                self.__class__.objects.get(pk=pk)
            except:
                return pk	

    return wrapped
    
