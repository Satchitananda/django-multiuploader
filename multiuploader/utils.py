import logging
log = logging
import os,datetime


from shutil import move
from django.conf import settings
from django.core.files import File
from models import MultiuploaderFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile


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
    for attach in MultiuploaderFile.objects.all():
        filepath = os.path.join(settings.MEDIA_ROOT,attach.file.name)      
        try:
            os.remove(filepath)
        except Exception as e:
            if print_to_console:
                print e

    MultiuploaderFile.objects.all().delete()
    if print_to_console:
        print "Cleaning temporary upload files complete"


        print "IDs:",attachmentIDs
        
        #attachmentsStrs = attachmentStr.split(";")
        files = MultiuploaderFile.objects.filter(id__in=attachmentIDs)
        
        #Moving each file to our specific directory
        for fl in files:
            oldpath = os.path.join(settings.MEDIA_ROOT,fl.file.name)
            path = pathToMove
    
            if not os.path.isdir(path):
                os.makedirs(path)

            newpath = os.path.join(path,os.path.basename(fl.file.name))
            move(oldpath,newpath)
            attach = attachmentClass.objects.create(file=newpath,upload_date=fl.upload_date,key_data=fl.key_data)
            ats.append(attach)
            
            #Removing old temp attachment
            if removeFromTemp:
                fl.delete()
                
    return ats

def move_uploaded_files(ids,pathToMove,attachmentClass,removeFromTemp=True):
    ats = []
    files = MultiuploaderFile.objects.filter(id__in=ids)
    
    #Moving each file to our specific directory
    for fl in files:
        oldpath = os.path.join(settings.MEDIA_ROOT,fl.file.name)
        path = pathToMove#os.path.join(settings.MEDIA_ROOT,settings.MESSAGE_ATTACHMENTS_PATH)

        if not os.path.isdir(path):
            os.makedirs(path)

        newpath = os.path.join(path,os.path.basename(fl.file.name))
        move(oldpath,newpath)
        
        attach = attachmentClass.objects.create(file=newpath,upload_date=fl.upload_date,key_data=fl.key_data)
        ats.append(attach)
        
        #Removing old temp attachment
        if removeFromTemp:
            fl.delete()
                
    return ats

    
def move_files_from_model(fromModel,toAttachmentModel,filesAttrName,pathToMove,removeOld = False):
    ats = []
    files = getattr(fromModel,filesAttrName)

    if not os.path.isdir(pathToMove):
        os.makedirs(pathToMove)
    
    for fl in files:
        oldpath = os.path.join(settings.MEDIA_ROOT,fl.file.name)
        newpath = os.path.join(pathToMove,os.path.basename(fl.file.name))
        move(oldpath,newpath)
        attach = toAttachmentModel.objects.create(file=newpath,upload_date=fl.upload_date,key_data=fl.key_data)
        ats.append(attach)
        
        #Remove the old
        if removeOld:
            fl.delete()
            
    return ats
