from django.contrib import admin
from .models import MyUser
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
@admin.register(MyUser)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email','mobile')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('id','username','email','mobile', 'first_name', 'last_name')