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

#------------------------------------------------------------------------------------
# Methods below this comment marked for deprecation
#------------------------------------------------------------------------------------

def move_uploads_from_temp(ids,pathToMove,removeFromTemp=False):
    """Method gets list of uploaded ids, pathToMove as relative path from MEDIA_ROOT, 
       returns list of file pathes of dict {path:'path',date:date,name:'filename'}
    """
    
    ats = []
    files = MultiuploaderFile.objects.filter(id__in=ids)
    
    #Moving each file to our specific directory
    for fl in files:
        oldpath = os.path.join(settings.MEDIA_ROOT,fl.file.name)
        path = pathToMove

        if not os.path.isdir(os.path.join(settings.MEDIA_ROOT,path)):
            os.makedirs(os.path.join(settings.MEDIA_ROOT,path))
        
        fileBaseName = os.path.basename(fl.file.name)
        newpath = os.path.join(settings.MEDIA_ROOT,path,fileBaseName)
        
        try:
            #print "Old:",oldpath,"New:",newpath,"Save:",os.path.join(path,fileBaseName)
            move(oldpath,newpath)
            
            #Adding a relative path to model
            ats.append({"path": os.path.join(path,fileBaseName),"date":fl.upload_date,"name":fl.filename})
        except Exception as e:
            print e
        
        #attach = attachmentClass.objects.create(file=newpath,upload_date=fl.upload_date,key_data=fl.key_data)
        #Removing old temp attachment
        
        if removeFromTemp:
            fl.delete()
                
    return ats


def move_uploads_from_model(fromModelEntity,filesAttrName,pathToMove,removeOld = False):
    """Replaces attachment files from model to a given location, 
       returns list of file pathes of dict {path:'path',date:date,name:'filename'}
    """
    
    ats = []
    files = getattr(fromModelEntity,filesAttrName)

    if not os.path.isdir(os.path.join(settings.MEDIA_ROOT,pathToMove)):
        os.makedirs(os.path.join(settings.MEDIA_ROOT,pathToMove))
    
    for fl in files:
        fileBaseName = os.path.basename(fl.file.name)
        oldpath = os.path.join(settings.MEDIA_ROOT,fl.file.name)
        newpath = os.path.join(settings.MEDIA_ROOT,pathToMove,fileBaseName)
        
        try:
            move(oldpath,newpath)
            #Adding a relative path to model
            ats.append(ats.append({"path":os.path.join(pathToMove,fileBaseName),"date":fl.upload_date,"name":fl.filename}))
        except Exception as e:
            print e
        
        #attach = toAttachmentModel.objects.create(file=newpath,upload_date=fl.upload_date,key_data=fl.key_data)
        #Remove the old from DB
       
        if removeOld:
            fl.delete()
            
    return ats

def load_files_from_request(request,pathToMove,noajax=False,storage=default_storage):
    ats = []
      
    if request.method == 'POST':
        if request.FILES == None:
            return []

        #getting file data for farther manipulations
        
        if not u'files' in request.FILES:
            return []
        
        for file in request.FILES.getlist("files"):
            wrapped_file = UploadedFile(file)
            filename = wrapped_file.name
            
            #Need a bit later to calculate all file count
            file_size = wrapped_file.file.size
            
            newpath = os.path.join(settings.MEDIA_ROOT,pathToMove,wrapped_file.name)
            fullname = storage.get_available_name(newpath)
            
            with open(newpath, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
              
            #fileBaseName = os.path.basename(wrapped_file.name)
            #oldpath = os.path.join(settings.FILE_UPLOAD_TEMP_DIR,wrapped_file.name)
            ats.append({"path":os.path.relpath(fullname,settings.MEDIA_ROOT),"date":datetime.datetime.now(),"name":wrapped_file.name})
          
        print ats
        return ats
    


#----------------------------------------------------------------------------
# All below this line is deprecated
#----------------------------------------------------------------------------

def form_move_uploaded_files(form,pathToMove,attachmentClass,removeFromTemp=True):
    ats = []
    attachmentIDs = form.cleaned_data["uploadedFiles"]
    
    if attachmentIDs:
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


    
