from django.conf import Settings

DEFAULTS =  Settings("multiuploader.default_settings")

VERSION = (1, 2, 0)
__version__ = '.'.join(map(str, VERSION))
