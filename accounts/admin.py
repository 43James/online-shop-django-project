from django.contrib import admin

from .models import MyUser, Profile

admin.site.register(MyUser)
admin.site.register(Profile)

# class MyUserAdmin(admin.ModelAdmin):
#     list_display = ['id','username','email','is_active','is_manager','is_admin']
#     list_filter = ['username']
#     search_fields = ['username']