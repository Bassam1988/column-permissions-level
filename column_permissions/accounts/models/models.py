import uuid
from django.db import models
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group

from django.dispatch import receiver

from pediahome_resetpassword.signals import reset_password_token_created

from datetime import datetime

from django.utils.crypto import get_random_string

from .custom_authorization_models import CustomGroup, CustomPermission

from custom_email.models import send_custom_email

from classes.GeneralFunctions import upload_path_profile, default_value


class UserStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_name = models.CharField(max_length=6)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def get_name(self):
        return self.name


# def _user_get_custom_permissions(user, obj, from_name):
#     permissions = set()
#     name = "get_%s_permissions" % from_name
#     for backend in auth.get_backends():
#         if hasattr(backend, name):
#             permissions.update(getattr(backend, name)(user, obj))
#     return permissions

class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    img = models.ImageField(blank=True, upload_to=upload_path_profile)
    # the user will consider as active if the value of this column not Ac
    status = models.ForeignKey(
        UserStatus, default=default_value(UserStatus), on_delete=models.SET(default_value(UserStatus)))
    custom_permission = models.ManyToManyField(
        CustomPermission, related_name="allowed_user", blank=True)
    custom_group = models.ManyToManyField(
        CustomGroup, related_name="group_user", blank=True)
    default_groups = models.ManyToManyField(
        Group, related_name="group_user", blank=True)
    default_custom_group = models.ManyToManyField(
        CustomGroup, related_name="default_group_user", blank=True)

    def __str__(self):
        return self.email

    @property
    def get_name(self):
        return self.first_name+" "+self.last_name

    @property
    def get_image(self):
        return self.img

    def get_task_type_permissions(self):
        task_type_permissions = CustomPermission.objects.none()
        allowed_task_types = self.pediahome_employee.active_contract.allowed_task.all()
        for task_type in allowed_task_types:
            custom_group = task_type.custom_groups
            task_type_permissions = task_type_permissions.union(
                custom_group.permission.all())
        return task_type_permissions

    def get_profile_permissions(self):
        profile_permissions = CustomPermission.objects.none()
        pediaHome_profile = self.pediaHome_profile
        industries = pediaHome_profile.industries.all()
        for industry in industries:
            profile_model = industry.profile_model_name
            industry_profile = getattr(pediaHome_profile, profile_model, None)
            if industry_profile:
                industry_profile_custom_group = industry_profile.profile_type.custom_groups.prefetch_related(
                    'permission').all()
                for custom_group in industry_profile_custom_group:
                    profile_permissions = profile_permissions.union(
                        custom_group.permission.all())
        return profile_permissions

    def _get_group_custom_permissions(self, from_name):
        user_groups_field = get_user_model()._meta.get_field(from_name)
        user_groups_query = "%s__%s" % (
            'custom_group', user_groups_field.related_query_name())
        return CustomPermission.objects.select_related('action').filter(**{user_groups_query: self})

    def get_custom_perm(self):
        perm_cache_name = "_custom_perm_cache"
        if not hasattr(self, perm_cache_name):
            # if self.is_active and self.is_superuser:
            #     perms = CustomPermission.objects.all()
            # else:
            perms = getattr(
                self, "_get_group_custom_permissions")('custom_group')
            perms = perms.union(getattr(
                self, "_get_group_custom_permissions")('default_custom_group'))

            if self.is_staff:
                perms = perms.union(self.get_task_type_permissions())
            else:
                perms = perms.union(self.get_profile_permissions())

            perms = perms.values_list(
                "action__request_method", "action__view_action", "app_label", "model", "column_name").order_by()
            setattr(
                self, perm_cache_name, {"%s.%s.%s.%s.%s" % (
                    mth_name, v_action, app_label, model.lower(), column_name) for mth_name, v_action, app_label, model, column_name in perms}
            )
        return getattr(self, perm_cache_name)

    # def get_group_permissions(self, obj=None):
    #     if obj:
    #         return super(CustomUser, self).get_group_permissions(obj)
    #     permissions = super(CustomUser, self).get_group_permissions()
    #     default_perms = set()
    #     default_groups = self.default_groups.all()
    #     if default_groups:
    #         for group in default_groups:
    #             for permission in group.permissions.all():
    #                 perm = permission.content_type.app_label+'.'+permission.codename
    #                 default_perms.add(perm)
    #     if permissions:
    #         return permissions.union(default_perms)
    #     return default_perms

    # def get_all_permissions(self, obj=None):
    #     if obj:
    #         return super(CustomUser, self).get_all_permissions(obj)
    #     permissions = super(CustomUser, self).get_all_permissions()
    #     default_perms = set()
    #     default_groups = self.default_groups.all()
    #     if default_groups:
    #         for group in default_groups:
    #             for permission in group.permissions.all():
    #                 perm = permission.content_type.app_label+'.'+permission.codename
    #                 default_perms.add(perm)
    #     if permissions:
    #         return permissions.union(default_perms)
    #     return default_perms

    # def has_perm(self, perm, obj=None):
    #     if self.is_active and self.is_superuser:
    #         return True
    #     has_pp = super(CustomUser, self).has_perm(perm, obj)
    #     if has_pp:
    #         return has_pp
    #     if not obj:
    #         if perm in self.get_all_permissions():
    #             return True
    #     return False

    # def has_perms(self, perm_list, obj=None):
    #     if self.is_active and self.is_superuser:
    #         return True
    #     has_pp = super(CustomUser, self).has_perms(perm_list, obj)
    #     if has_pp:
    #         return has_pp
    #     if not obj:
    #         permissions = self.get_all_permissions()
    #         for perm in perm_list:
    #             if perm not in permissions:
    #                 return False
    #         return True
    #     return False

    # def has_module_perms(self, package_name):
    #     if self.is_active and self.is_superuser:
    #         return True
    #     has_pp = super(CustomUser, self).has_module_perms(package_name)
    #     if has_pp:
    #         return has_pp
    #     permissions = self.get_all_permissions()
    #     for perm in permissions:
    #         if package_name == perm.split('.')[0]:
    #             return True

    @property
    def is_authenticated(self):
        if hasattr(self, 'pediahome_employee'):
            active_contract = self.pediahome_employee.contracts.filter(start_date__lte=datetime.today(
            ), end_date__gte=datetime.today(), contract_status__code_name='AT')
            if active_contract:
                return True
            else:
                return False
        return True


UserModel = get_user_model()

# class CustomContentType(ContentType):


class ChangePasswordCode(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=6, default=get_random_string(length=6,))
    active = models.BooleanField(default=1)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    send_custom_email(reset_password_token, 'CtRP')
