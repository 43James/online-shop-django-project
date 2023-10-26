from django.contrib import admin

from .models import MyUser, Profile

class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','is_active','is_manager','is_admin']
    list_filter = ['username']
    search_fields = ['username']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','work_group','position']

admin.site.register(MyUser,MyUserAdmin)
admin.site.register(Profile,ProfileAdmin)