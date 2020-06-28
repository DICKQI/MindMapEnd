from django.contrib import admin
from .models import MindMap, MindMapCoMember


# Register your models here.

@admin.register(MindMap)
class AdminMindMap(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['mapId', 'mapName', 'roomMaster', 'shareStatus', 'create_date', 'last_mod_date']


@admin.register(MindMapCoMember)
class AdminMindMapCoMember(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['map', 'user', 'auth']
