from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import MyUser, Profile, WorkGroup

class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','is_active','is_manager','is_admin',]
    list_filter = ['username']
    search_fields = ['username']

admin.site.register(MyUser,MyUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','workgroup','position']

admin.site.register(Profile,ProfileAdmin)


class WorkGroupAdmin(admin.ModelAdmin):
    list_display = ['id','work_group']

admin.site.register(WorkGroup,WorkGroupAdmin)
