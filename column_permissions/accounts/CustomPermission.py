from django.conf import settings
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import exceptions


class PediahomePermission(DjangoModelPermissions):
    SAFE_METHODS = []
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],  # permission changed
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        method = request.method
        if hasattr(view, 'SAFE_METHODS') and method in view.SAFE_METHODS:
            return True
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True
        user = request.user
        if not user or (
           not user.is_authenticated and self.authenticated_users_only):
            return False

        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        has_fields_perm = self.get_fields(request, view)
        return has_fields_perm

    def has_object_permission(self, request, view, obj):
        try:
            user = request.user
            method = request.method
            owner = getattr(obj, 'get_owner', None)
            if owner:
                forbidden_apps = settings.FORBIDDEN_APPS
                # we  added this condition because if user has DW entity profile he can view and update Entity objects,
                # but it should not update any profile other its profile
                # if method.lower() == 'get':
                #     self.get_field(request, view, True)
                app_name = obj._meta.app_label
                has_fields_perm = False
                if owner == user or (user.is_staff and app_name not in forbidden_apps):
                    has_fields_perm = self.get_fields(request, view, True)
                elif method.lower() == 'get':
                    has_fields_perm = self.get_fields(request, view)
                else:
                    return has_fields_perm
            else:  # if the object doesn't has owner attr, we will return the user custom pemission
                has_fields_perm = self.get_fields(request, view)
            return has_fields_perm
        except Exception as e:
            raise e

    def check_custom_permission(self, user, app_label, table_name, fields, method, view):
        action = view.action
        action_list = ['retrieve', 'list', 'destroy',
                       'partial_update', 'update', 'create']
        methods = ['get']
        method_lower = method.lower()
        if method.lower() != 'get':
            methods.append(method_lower)

        user_group_permission = user.get_custom_perm()
        # user_group_permission = user_group_permission.union(
        #     user.get_custom_perm('default_custom_group'))

        allowed_permissions = set()
        allowed_display_permissions = set()

        if action in action_list:
            if method_lower != 'get':
                for user_permission in user_group_permission:
                    split_user_perm = user_permission.split('.')
                    if split_user_perm[1] == action and split_user_perm[2] == app_label and split_user_perm[3] == table_name.lower():
                        allowed_permissions.add(split_user_perm[4])
                for user_permission in user_group_permission:
                    split_user_perm = user_permission.split('.')
                    if split_user_perm[1] == 'retrieve' and split_user_perm[2] == app_label and split_user_perm[3] == table_name.lower():
                        allowed_display_permissions.add(split_user_perm[4])
            else:
                for user_permission in user_group_permission:
                    split_user_perm = user_permission.split('.')
                    if split_user_perm[1] == action and split_user_perm[2] == app_label and split_user_perm[3] == table_name.lower():
                        allowed_permissions.add(split_user_perm[4])
        else:
            try:
                pk = view.kwargs['pk']
                if method_lower != 'get':
                    for user_permission in user_group_permission:
                        split_user_perm = user_permission.split('.')
                        if split_user_perm[0] == method_lower and split_user_perm[2] == app_label and split_user_perm[3] == table_name.lower():
                            allowed_permissions.add(split_user_perm[4])
                    for user_permission in user_group_permission:
                        split_user_perm = user_permission.split('.')
                        if split_user_perm[1] == 'retrieve' and split_user_perm[2] == app_label and split_user_perm[3] == table_name.lower():
                            allowed_display_permissions.add(split_user_perm[4])
                else:
                    for user_permission in user_group_permission:
                        split_user_perm = user_permission.split('.')
                        if split_user_perm[1].find(method_lower) == 'retrieve' and split_user_perm[2] == app_label and split_user_perm[3] == table_name.lower():
                            allowed_permissions.add(split_user_perm[4])
            except:
                if method_lower != 'get':
                    for user_permission in user_group_permission:
                        split_user_perm = user_permission.split('.')
                        if split_user_perm[0] == method_lower and split_user_perm[2] == app_label and split_user_perm[3] == table_name.lower():
                            allowed_permissions.add(split_user_perm[4])
                    for user_permission in user_group_permission:
                        split_user_perm = user_permission.split('.')
                        if split_user_perm[1] == 'list' and split_user_perm[2] == app_label and split_user_perm[3] == table_name.lower():
                            allowed_display_permissions.add(split_user_perm[4])
                else:
                    for user_permission in user_group_permission:
                        split_user_perm = user_permission.split('.')
                        if split_user_perm[1] == 'list' and split_user_perm[2] == app_label and split_user_perm[3] == table_name.lower():
                            allowed_permissions.add(split_user_perm[4])

        return allowed_permissions, allowed_display_permissions

    def get_fields(self, request, view, owner=False):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        queryset = self._queryset(view)
        model = queryset.model
        app_label = model._meta.app_label
        model_name = model.__name__
        user = request.user
        method = request.method
        forbidden_apps = settings.FORBIDDEN_APPS

        if user.is_active and user.is_superuser:
            view.fields = '__all__'
            view.display_fields = '__all__'
            return True

        allowed_perm, allowed_display_perm = self.check_custom_permission(
            user, app_label, model_name, [], method, view)
        if allowed_perm:
            view.fields = list(allowed_perm)
            if allowed_display_perm and len(allowed_display_perm) > len(allowed_perm):
                allowed_display_fields = allowed_display_perm
            else:
                allowed_display_fields = allowed_perm
            if ((user.is_staff and app_label not in forbidden_apps) or owner) and view.action == 'retrieve':
                view.display_fields = '__all__'
            else:
                view.display_fields = list(allowed_display_fields)
            return True
        else:
            return False
