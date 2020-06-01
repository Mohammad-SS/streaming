from django.contrib import admin
from streaming.models import Archive, ConductorItem, User
# Register your models here.

admin.site.register(Archive)
admin.site.register(ConductorItem)
admin.site.register(User)
