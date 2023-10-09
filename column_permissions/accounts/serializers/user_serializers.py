
from django.contrib.auth import password_validation
from rest_framework import serializers, status
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


from datetime import timedelta, datetime
from apps.accounts.validators import UnicodeUsernameValidator

from apps.classes.GeneralFunctions import general_update

from ..models.models import UserModel, ChangePasswordCode


# User Serializer
"""
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'img')
"""


class UserSerializer(serializers.ModelSerializer):
    # profile = UserProfileSerializer(required=True)
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password',
                  'img', 'custom_permission', 'custom_group', 'default_groups', 'default_custom_group')
        extra_kwargs = {'password': {'write_only': True},
                        'default_groups': {'read_only': True},
                        'default_custom_group': {'read_only': True},

                        }

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(UserSerializer, self).__init__(*args, **kwargs)
        # super().__init__(self,data=data)
        if fields:
            self.Meta.fields = fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        img = representation.pop('img', None)
        custom_permission = representation.pop('custom_permission', None)
        custom_group = representation.pop('custom_group', None)
        default_groups = representation.pop('default_groups', None)
        default_custom_group = representation.pop('default_custom_group', None)
        if instance.is_staff and hasattr(instance, 'pediahome_employee'):
            employee_profile = instance.pediahome_employee
            try:
                employee_type = employee_profile.employee_type
            except Exception as e:
                employee_type = None
            try:
                employee_active_contract = employee_profile.active_contract
            except Exception as e:
                employee_active_contract = None

            if employee_type:
                industries = employee_type.ph_industry.all()
                industries_data = []
                for industry in industries:
                    industry_id = industry.id
                    industry_code_name = industry.code_name
                    industry_name = industry.name
                    industry_data = {"industry_id": industry_id,
                                     "industry_code_name": industry_code_name, "industry_name": industry_name}
                    industries_data.append(industry_data)
                employee_type_level = employee_type.level
                can_add_user = employee_type_level.can_add_user
                can_add_task = employee_type_level.can_add_task
            else:
                industries_data = None
                employee_type_level = None
                can_add_user = None
                can_add_task = None
            art_categories = []
            if employee_active_contract:
                contract_tasks = employee_active_contract.allowed_task.all()
                contract_tasks_data = []
                for task in contract_tasks:
                    task_id = task.id
                    task_code_name = task.code_name
                    task_data = {"task_id": task_id,
                                 "task_code_name": task_code_name}
                    task_perms = []
                    custom_group = task.custom_groups
                    if custom_group:
                        custom_permissions = custom_group.permission.all()
                        for custom_permission in custom_permissions:
                            perm_id = custom_permission.id
                            perm_code_name = custom_permission.code_name
                            perm_action = custom_permission.action.code_name
                            perm_column_name = custom_permission.column_name
                            perm_data = {"perm_id": perm_id, "perm_code_name": perm_code_name,
                                         "perm_action": perm_action, "perm_column_name": perm_column_name}
                            task_perms.append(perm_data)
                        task_data["task_perms"] = task_perms
                    contract_tasks_data.append(task_data)
                art_categories_data = employee_active_contract.art_category.all()

                for art_category_data in art_categories_data:
                    art_category = {'id': art_category_data.id,
                                    'name': art_category_data.name}
                    art_categories.append(art_category)
            else:
                contract_tasks_data = None
            employee_profile_data = {}
            """
            childs_queryset = employee_profile.employee_type.child.all()
            childs = []
            for child_data in childs_queryset:
                child = {'id': child_data.id, 'name': child_data.name}
                childs.append(child)
            employee_type = {'id': employee_profile.employee_type.id, 'name': employee_profile.employee_type.name,
                              'child': childs}

            allowed_languages_data = employee_profile.can_write.all()
            allowed_languages = []
            if allowed_languages_data:
                for allowed_language_data in allowed_languages_data:
                    allowed_languages.append(
                        {'id': allowed_language_data.id,
                         'source_language': {"id": allowed_language_data.source_language.id, "name": allowed_language_data.source_language.name},
                         'destination_language': {"id": allowed_language_data.destination_language.id, "name": allowed_language_data.destination_language.name}})
            """

            # employee_profile_data['employee_type'] = employee_type
            # employee_profile_data['allowed_language'] = allowed_languages
            employee_profile_data['art_category'] = art_categories

            return {
                'id': instance.id,
                'is_staff': instance.is_staff,
                'username': instance.username,
                'email': instance.email,
                'first_name': instance.first_name,
                'last_name': instance.last_name,
                'img': img,
                # 'custom_permission': custom_permission,
                # 'custom_group': custom_group,
                # 'default_groups': default_groups,
                # 'default_custom_group': default_custom_group,
                "contract_tasks_data": contract_tasks_data,
                'pediahome_employee': employee_profile_data,
                "industry": industries_data,
                "can_add_user": can_add_user,
                "can_add_task": can_add_task,
            }
        return {
            'id': instance.id,
            'is_staff': instance.is_staff,
            'username': instance.username,
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'img': img,
            'custom_permission': custom_permission,
            'custom_group': custom_group

        }

    """
    def create(self, validated_data):
        custom_permission = None
        custom_group = None
        try:
            custom_permission = validated_data.pop('custom_permission')
        except:
            pass

        try:
            custom_group = validated_data.pop('custom_group')
        except:
            pass

        user = CustomUser.objects.create(**validated_data)

        if custom_permission:
            user.custom_permission.set(custom_permission)

        if custom_group:
            user.custom_group.set(custom_group)

        user.save()
    """


class UserListField(serializers.RelatedField):
    def to_representation(self, value):
        return {"username": value.username, "email": value.email, "first_name": value.first_name, "last_name": value.last_name}

# Register Serializer


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'email', 'password',
                  'first_name', 'last_name', 'is_staff', 'status')
        extra_kwargs = {'password': {'write_only': True},
            'email': {'validators': []},
            'username': {'validators': [UnicodeUsernameValidator()]},
        }

    def validate(self, data):
        request = self.context.get('request')
        request_method = request.method
        instance = self.instance

        email = data.get('email', instance.email if instance else None)
        username = data.get('username', instance.username if instance else None)

        if request_method == "POST":

            if UserModel.objects.filter(email=email).exists():
                raise serializers.ValidationError({'email': ["This email is already in use."]})

            if UserModel.objects.filter(username=username).exists():
                raise serializers.ValidationError({'username': ["This username is already in use."]})
            password = data['password']
            password_validation.validate_password(password)

        elif request_method == "PUT" or request_method == "PATCH":
            if instance:
                if UserModel.objects.filter(email=email).exclude(pk=instance.pk).exists():
                    raise serializers.ValidationError({'email': ["This email is already in use."]})

                if UserModel.objects.filter(username=username).exclude(pk=instance.pk).exists():
                    raise serializers.ValidationError({'username': ["This username is already in use."]})

        return data

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)

        return user
    


# Login Seriliazer


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def login(self, data):
        user = authenticate(**data)
        if user and user.is_active and user.status.code_name == 'Ac':
            return user
        raise AuthenticationFailed('Invalid username or password.')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirmation = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
    t_delta = timedelta(minutes=180)

    class Meta:
        model = UserModel
        fields = ['password']

    def validate(self, data):
        validated_data = super(ChangePasswordSerializer, self).validate(data)
        request = self.context['request']
        user = request.user
        confirmation_code = validated_data["confirmation_code"]

        confirmation_code = ChangePasswordCode.objects.filter(
            user=user, code=confirmation_code, created_date__gte=datetime.now()-self.t_delta, active=1).exists()
        if confirmation_code:
            old_password = validated_data["old_password"]
            if not user.check_password(old_password):
                raise serializers.ValidationError(
                    {"old_password": ["Wrong password."], "status": status.HTTP_400_BAD_REQUEST})

            new_password = validated_data["new_password"]
            new_password_confirmation = validated_data["new_password_confirmation"]
            if old_password == new_password:
                raise serializers.ValidationError(
                    {"new_password": "the new password and the old password are match"})
            if new_password == new_password_confirmation:
                password_validation.validate_password(new_password)
                return validated_data
            raise serializers.ValidationError(
                {"new_password": "the new password and the new password confirmation don't match"})
        else:
            raise serializers.ValidationError(
                {"confirmation_code": "the confirmation code is invalid"})

    def update(self, instance, validated_data):
        user = instance
        password = validated_data['new_password']
        user.set_password(password)
        user.save()
        confirmation_code = validated_data['confirmation_code']
        confirmation_code = ChangePasswordCode.objects.filter(
            user=user, code=confirmation_code, created_date__gte=datetime.now()-self.t_delta, active=1)
        confirmation_code.active = 0
        confirmation_code.save()

        return True


class ChangePasswordCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangePasswordCode
        fields = ['user', 'code']

    def create(self, data):
        user = data['user']
        pass_code = ChangePasswordCode.objects.create(user=user)
        return pass_code
