from django.conf import settings,Settings
from django.conf.urls.defaults import patterns, url

DEFAULTS = Settings("multiuploader.default_settings")

urlpatterns = patterns('',
    url(r'^multi_delete/(?P<id>\w+)/$', 'multiuploader.views.multiuploader_delete', name='multi_delete'),
    url(r'^multi/$', 'multiuploader.views.multiuploader', name='multi'),
    url(r'^multi_noajax/$', 'multiuploader.views.multiuploader',kwargs={"noajax":True},name='multi_noajax'),
    url(r'^multi_file/(?P<pk>\w+)/$', 'multiuploader.views.multi_show_uploaded',name='multi_file_link'),
)
