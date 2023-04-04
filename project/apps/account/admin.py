from django.contrib import admin
from .models import Profile,PasswordResetCount,LoginCount

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']

@admin.register(PasswordResetCount)
class PasswordResetCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'count')

@admin.register(LoginCount)
class LoginCountAdmin(admin.ModelAdmin):
    list_display = ['id', 'count']
