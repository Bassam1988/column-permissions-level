from django.contrib.contenttypes.models import ContentType
from asgiref.sync import sync_to_async
from django.conf import settings
from django.apps import apps
from rest_framework import serializers


from ..models.custom_authorization_models import CustomGroup, CustomPermission, PermissionAction


class PermissionActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionAction
        fields = ['id', 'name', 'description', 'code_name']
        extra_kwargs = {'code_name': {'write_only': True}}


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['id', 'app_label', 'model']

    def to_representation(self, instance):
        fields_name = []
        m_instance = instance.model_class()
        if m_instance:
            fields = m_instance._meta.fields

            for field in fields:
                fields_name.append(field.name.split('.')[-1])

        return {
            'id': instance.id,
            'app_label': instance.app_label,
            'model': instance.model,
            'fields_name': fields_name,
        }

    def get_model_fields(self, instance):
        m_instance = instance.model_class()
        fields = m_instance._meta.fields
        fields_name = []
        for field in fields:
            fields_name.append(field.name.split('.')[-1])
        return fields_name


class CustomPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomPermission
        fields = '__all__'

    def to_representation(self, instance):

        return {
            'id': instance.id,
            'table_info': {'id': instance.content_type.id, 'app_label': instance.content_type.app_label, 'model': instance.content_type.model, 'name': instance.content_type.name, },
            'content_type': ContentTypeSerializer(instance.content_type).data,
            'action': instance.action.name,
            'column_name': instance.column_name,
        }

    @sync_to_async
    def get_content_type(self, app_label, model_name):
        return ContentType.objects.get(app_label=app_label, model=model_name)

    @sync_to_async
    def abulk_create(self, new_custom_permissions_list):
        return CustomPermission.objects.abulk_create(
            new_custom_permissions_list,
            update_conflicts=True,
            unique_fields=["action", "column_name", "app_label", "model"],
            update_fields=["name", "code_name", "description"],
        )

    @sync_to_async
    def get_action_list(self):
        return list(PermissionAction.objects.all())

    async def create_custom_permissions_new_tables(self):
        try:
            new_custom_permissions_list = []
            exists_check_perm = []
            action_list = await self.get_action_list()  # PermissionAction.objects.all()
            # action_list_code_name=[action.id for action in action_list]
            # exists_perms = CustomPermission.objects.all()
            created_apps = settings.CREATED_APPS
            list_of_apps = [apps.get_app_config(app_name.split('.')[-1])
                            for app_name in created_apps]
            now_app = None
            now_model = None
            perm_count = 0
            for app in list_of_apps:
                now_app = app
                app_name = app.name.split('.')[-1]
                models_list = [model for name, model in app.models.items(
                ) if not model._meta.auto_created]
                for model in models_list:
                    now_model = model
                    model_name = model.__name__.lower()
                    content_type = await ContentType.objects.aget(
                        app_label=app_name, model=model_name)
                    fields = model._meta.get_fields()
                    fields_name = [field.name for field in fields]
                    for field_name in fields_name:
                        for action in action_list:
                            # check_perm = exists_perms.filter(
                            #     content_type=content_type, column_name=field_name, action=action).exists()
                            # if True:# not check_perm:
                            name = action.name+' '+action.view_action+' ' + \
                                ' ' + app_name+' '+model_name+' ' + field_name
                            sub_app_name = app_name[:2]
                            if app_name.find('_'):
                                app_name_list = app_name.split('_')
                                sub_app_name = ''
                                for sub in app_name_list:
                                    sub_app_name += sub[:2]
                            description = name

                            code_name = action.code_name + \
                                sub_app_name + \
                                model_name[:2]+field_name+str(content_type.id)
                            perm_count += 1
                            permission = CustomPermission(
                                name=name, code_name=code_name, column_name=field_name, description=description, app_label=app_name, model=model_name, action=action, content_type=content_type)
                            new_custom_permissions_list.append(permission)

            objs = await CustomPermission.objects.abulk_create(
                new_custom_permissions_list, update_conflicts=True,
                unique_fields=[
                    'action', 'column_name', 'app_label', 'model'],
                update_fields=['name', 'code_name', 'description'])

            return objs, perm_count
        except Exception as e:
            return str(e.args)+" app:"+now_app+" model:"+now_model


class CustomGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomGroup
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        permissions_data = instance.permission.all()
        permissions = []
        if permissions_data:
            for permission in permissions_data:

                permissions.append({'id': permission.id, 'name': permission.name, 'column_name': permission.column_name,
                                   'action': permission.action.name, 'content_type': ContentTypeSerializer(permission.content_type).data, })

        return {
            'id': instance.id,
            'name': instance.name,
            'permission': permissions,
        }
    """
    def create(self, validated_data):
        permission = None

        try:
            permission=validated_data.pop('permission')
        except:
            pass

        custom_group = CustomGroup.objects.create(**validated_data)
        if permission:
            custom_group.permission.set(permission)
            custom_group.save()
        return custom_group
    """
