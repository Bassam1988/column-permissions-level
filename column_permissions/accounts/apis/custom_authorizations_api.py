from django.contrib.contenttypes.models import ContentType

from rest_framework import permissions, viewsets, status

from ..serializers.custom_authorization_serializers import PermissionActionSerializer, ContentTypeSerializer, CustomPermissionSerializer,\
    CustomGroupSerializer

from ..models.custom_authorization_models import PermissionAction, CustomGroup, CustomPermission

from apps.classes.CustomResponse import CustomResponse


class PermissionActionViewSet(viewsets.ModelViewSet):

    serializer_class = PermissionActionSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or (hasattr(user, 'pediahome_employee') and user.pediahome_employee.contracts.get(contract_status__code_name="AT").employee_type.can_add_user):
            return PermissionAction.objects.all()
        else:
            return PermissionAction.objects.none()

    def create(self, request):
        user = request.user
        if user.is_superuser:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = {"permission_action": serializer.data}
                    return CustomResponse(succeeded=True, message='', data=data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return CustomResponse(succeeded=False, message='please try again: ' + str(e.args), data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return CustomResponse(succeeded=False, message=serializer.errors, data={}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        user = request.user
        if user.is_superuser:
            permission_action = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(
                permission_action, data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = {"permission_action": serializer.data}
                    return CustomResponse(succeeded=True, message='', data=data, status=status.HTTP_200_OK)
                except Exception as e:
                    return CustomResponse(succeeded=False, message='please try again: ' + str(e.args), data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return CustomResponse(succeeded=False, message=serializer.errors, data={}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        user = request.user
        if user.is_superuser:
            permission_action = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(
                permission_action, data=request.data, partial=True)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = {"permission_action": serializer.data}
                    return CustomResponse(succeeded=True, message='', data=data, status=status.HTTP_200_OK)
                except Exception as e:
                    return CustomResponse(succeeded=False, message='please try again: ' + str(e.args), data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return CustomResponse(succeeded=False, message=serializer.errors, data={}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)


class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ContentTypeSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ContentType.objects.all()
        else:
            return ContentType.objects.none()

    def create(self, request):
        return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)


class CustomPermissionViewSet(viewsets.ModelViewSet):

    serializer_class = CustomPermissionSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CustomPermission.objects.all()
        elif (hasattr(user, 'pediahome_employee') and user.pediahome_employee.contracts.get(contract_status__code_name="AT").employee_type.can_add_user):
            return user.pediahome_employee.allowed_custom_permissions.all()

    def create(self, request):
        user = request.user
        if user.is_superuser:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = {"custom_permission": serializer.data}
                    return CustomResponse(succeeded=True, message='', data=data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return CustomResponse(succeeded=False, message='please try again: ' + str(e.args), data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return CustomResponse(succeeded=False, message=serializer.errors, data={}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        user = request.user
        if user.is_superuser:
            custom_permission = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(
                custom_permission, data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = {"custom_permission": serializer.data}
                    return CustomResponse(succeeded=True, message='', data=data, status=status.HTTP_200_OK)
                except Exception as e:
                    return CustomResponse(succeeded=False, message='please try again: ' + str(e.args), data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return CustomResponse(succeeded=False, message=serializer.errors, data={}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        user = request.user
        if user.is_superuser:
            custom_permission = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(
                custom_permission, data=request.data, partial=True)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = {"custom_permission": serializer.data}
                    return CustomResponse(succeeded=True, message='', data=data, status=status.HTTP_200_OK)
                except Exception as e:
                    return CustomResponse(succeeded=False, message='please try again: ' + str(e.args), data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return CustomResponse(succeeded=False, message=serializer.errors, data={}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)


class CustomGroupViewSet(viewsets.ModelViewSet):

    serializer_class = CustomGroupSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CustomGroup.objects.all()
        elif (hasattr(user, 'pediahome_employee') and user.pediahome_employee.contracts.get(contract_status__code_name="AT").employee_type.can_add_user):
            return user.pediahome_employee.contracts.get(contract_status__code_name="AT").employee_type.allowed_groups.all()

    def create(self, request):
        user = request.user
        if user.is_superuser:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = {"custom_group": serializer.data}
                    return CustomResponse(succeeded=True, message='', data=data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return CustomResponse(succeeded=False, message='please try again: ' + str(e.args), data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return CustomResponse(succeeded=False, message=serializer.errors, data={}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        user = request.user
        if user.is_superuser:
            custom_group = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(custom_group, data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = {"custom_group": serializer.data}
                    return CustomResponse(succeeded=True, message='', data=data, status=status.HTTP_200_OK)
                except Exception as e:
                    return CustomResponse(succeeded=False, message='please try again: ' + str(e.args), data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return CustomResponse(succeeded=False, message=serializer.errors, data={}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        user = request.user
        if user.is_superuser:
            custom_group = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(
                custom_group, data=request.data, partial=True)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = {"custom_group": serializer.data}
                    return CustomResponse(succeeded=True, message='', data=data, status=status.HTTP_200_OK)
                except Exception as e:
                    return CustomResponse(succeeded=False, message='please try again: ' + str(e.args), data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return CustomResponse(succeeded=False, message=serializer.errors, data={}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        return CustomResponse(succeeded=False, message="You don't have permission to do this action", data={}, status=status.HTTP_403_FORBIDDEN)
