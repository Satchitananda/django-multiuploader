from django.conf.urls.defaults import patterns, url
from django.conf import settings

try:
    delete_url = settings.MULTI_FILE_DELETE_URL
except AttributeError:
    delete_url = 'multi_delete'

try:
    file_url = settings.MULTI_FILE_URL
except AttributeError:
    file_url = 'multi_file'

urlpatterns = patterns('',
    url(r'^'+delete_url+'/(?P<pk>\d+)/$', 'multiuploader.views.multiuploader_delete', name='multi-delete'),
    url(r'^multi/$', 'multiuploader.views.multiuploader', name='multi'),
    url(r'^multi_noajax/$', 'multiuploader.views.multiuploader',kwargs={"noajax":True},name='multi_noajax'),
    url(r'^'+file_url+'/(?P<pk>\d+)/$', 'multiuploader.views.multi_show_uploaded',name='multi-file-link'),
)
