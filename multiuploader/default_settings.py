MULTIUPLOADER_ALLOWED_FILE_TYPES = ["txt","zip","jpg","jpeg","flv","png"]

MULTIUPLOADER_CONTENT_TYPES = [
                 'image/jpeg',
                 'image/png',
                 'application/msword',
                 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                 'application/vnd.ms-excel',
                 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                 'application/vnd.ms-powerpoint',
                 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                 'application/vnd.oasis.opendocument.text',
                 'application/vnd.oasis.opendocument.spreadsheet',
                 'application/vnd.oasis.opendocument.presentation',
                 'text/plain',
                 'text/rtf',
                ]

MULTIUPLOADER_MAX_FILE_SIZE = 10485760
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160

MULTIUPLOADER_MAX_FILE_NUMBER = 5

# Expiration time in seconds, one hour as default
MULTIUPLOADER_FILE_EXPIRATION_TIME = 3600

MULTIUPLOADER_FILES_FOLDER = 'multiuploader'
