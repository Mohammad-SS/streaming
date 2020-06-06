from django.contrib import admin
from streaming.models import Archive, ConductorItem, User , Temp
# Register your models here.

admin.site.register(Archive)
admin.site.register(ConductorItem)
admin.site.register(User)
admin.site.register(Temp)

