from django.contrib import admin
from .models import UserInfo

# Register your models here.

@admin.register(UserInfo)
class AdminUserInfo(admin.ModelAdmin):
    list_per_page = 50
    list_display = ['nickname', 'email', 'join_date']