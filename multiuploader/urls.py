from django.conf import settings,Settings
from django.conf.urls.defaults import patterns, url


DEFAULTS = Settings("multiuploader.default_settings")

delete_url = getattr(settings,"MULTI_FILE_DELETE_URL",DEFAULTS.MULTI_FILE_DELETE_URL)
file_url = getattr(settings,"MULTI_FILE_URL",DEFAULTS.MULTI_FILE_URL)

urlpatterns = patterns('',
    url(r'^'+delete_url+'/(?P<id>\d+)/$', 'multiuploader.views.multiuploader_delete', name='multi-delete'),
    url(r'^multi/$', 'multiuploader.views.multiuploader', name='multi'),
    url(r'^multi_noajax/$', 'multiuploader.views.multiuploader',kwargs={"noajax":True},name='multi_noajax'),
    url(r'^'+file_url+'/(?P<pk>\d+)/$', 'multiuploader.views.multi_show_uploaded',name='multi-file-link'),
)
