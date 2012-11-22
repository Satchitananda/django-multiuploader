from models import MultiuploaderFile
from django.contrib import admin

class MultiuploaderAdmin(admin.ModelAdmin):
    search_fields = ["filename", "key_data"]
    list_display = ["filename", "file",]
    list_filter = ["filename", "file"]

admin.site.register(MultiuploaderFile, MultiuploaderAdmin)