from django.conf import Settings

DEFAULTS =  Settings("multiuploader.default_settings")

VERSION = (0, 2, 0)
__version__ = '.'.join(map(str, VERSION))
