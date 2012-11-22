from django.core.management.base import BaseCommand, CommandError
#from multiuploader.models import MultiUploaderFile
from multiuploader.utils import cleanAttachments

class Command(BaseCommand):
    help = 'Clean all temporary attachments loaded to MultiuploaderFile model'

    def handle(self, *args, **options):
        cleanAttachments(True)
