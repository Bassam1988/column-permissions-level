
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q



UserModel = get_user_model()


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.prefetch_related('pediahome_employee__active_contract__allowed_task__custom_groups', 'pediaHome_profile__industries'
                                                      , 'custom_group__permission', 'default_custom_group__permission').select_related(
                'status').get(Q(username__iexact=username) | Q(email__iexact=username))
           
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(
                email__iexact=username)).order_by('id').first()

        if user.check_password(password) and self.user_can_authenticate(user) and user.status.code_name == 'Ac':
            if user.is_superuser:
                return user
            if user.is_staff:
                active_contract = user.pediahome_employee.active_contract
                if active_contract:
                    return user
                else:
                    return None
            return user

    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.prefetch_related('pediahome_employee__active_contract__allowed_task__custom_groups', 'pediaHome_profile__industries',
                                                               'custom_group__permission', 'default_custom_group__permission'
                                                               ).select_related('status').get(pk=user_id)

        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

    # def _get_custom_permissions(self, user_obj, obj, from_name):
    #     """
    #     Return the custom_permissions of `user_obj` from `from_name`. `from_name` can
    #     be either "custom_group" or "defualt_custom_group" to return permissions from
    #     `_get_custom_group_permissions` or `_get_default_custom_group_permissions` respectively.
    #     """
    #     if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
    #         return set()

    #     perm_cache_name = "_%s_perm_cache" % from_name
    #     if not hasattr(user_obj, perm_cache_name):
    #         if user_obj.is_superuser:
    #             perms = CustomPermission.objects.all()
    #         else:
    #             perms = getattr(self, "_get_%s_permissions" % from_name)(user_obj)
    #         perms = perms.values_list("content_type__app_label", "codename").order_by()
    #         setattr(
    #             user_obj, perm_cache_name, {"%s.%s" % (ct, name) for ct, name in perms}
    #         )
    #     return getattr(user_obj, perm_cache_name)
