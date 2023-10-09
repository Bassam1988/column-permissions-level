import uuid
from django.db import models
from django.db.models import UniqueConstraint

from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

from classes.GeneralFunctions import default_value


class PermissionAction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    code_name = models.CharField(max_length=50)
    request_method = models.CharField(max_length=15, default="d", null=False)
    view_action = models.CharField(max_length=40, default="d", null=False)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['code_name'],
                             name='unique_permission_action_code_name'),
            
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def get_name(self):
        return self.name


class CustomPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=500)
    code_name = models.CharField(max_length=120, unique=True)
    column_name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name='custom_permissions', default='1')
    action = models.ForeignKey(
        PermissionAction, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['action', 'column_name', 'app_label','model'],
                             name='unique_permission_action_column_app_model'),
            
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def get_name(self):
        return self.name


class GroupStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    code_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['code_name'],
                             name='unique_group_status_code_name'),
            UniqueConstraint(
                fields=['name'], name='unique_group_status_name')
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def get_name(self):
        return self.name


class CustomGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    code_name = models.CharField(max_length=10, unique=True)
    permission = models.ManyToManyField(
        CustomPermission, related_name='custom_group')
    description = models.CharField(max_length=500)
    status = models.ForeignKey(GroupStatus, null=True, on_delete=models.SET_NULL)
    auth_group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def get_columns(self):
        columns = []
        [columns.append(p.column_name)
         for p in self.permission.all() if p.column_name not in columns]
        return columns

    def __str__(self) -> str:
        return str(self.id)+" " + self.name

    @property
    def get_name(self):
        return self.name
