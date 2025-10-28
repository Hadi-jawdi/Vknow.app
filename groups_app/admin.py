from django.contrib import admin

# Register your models here.


from .import models

admin.site.register(models.GroupMember)
admin.site.register(models.GroupMessage)
admin.site.register(models.StudyGroup)