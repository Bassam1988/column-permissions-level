from django.contrib import admin
from django.contrib.auth import get_user_model 
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, CustomGroup, CustomPermission, PermissionAction, GroupStatus


class CustomUserAdmin(UserAdmin):    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = get_user_model()
    list_display = ['email']
    
    
#admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), CustomUserAdmin)


admin.site.register(CustomPermission)
admin.site.register(CustomGroup)
admin.site.register(GroupStatus)
admin.site.register(PermissionAction)
admin.site.register(Permission)


