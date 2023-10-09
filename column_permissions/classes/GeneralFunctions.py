from django.contrib.contenttypes.models import ContentType
import uuid
# from uuid import UUID
from datetime import datetime, date
from django.contrib.auth.hashers import make_password
from django.utils.module_loading import import_string
from classes.CustomResponse import CustomResponse
from rest_framework import serializers, status
from django.core.validators import MaxValueValidator, MinValueValidator

from classes.GeneralVariables import *


def current_year():
    return datetime.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


def check_required_fields(validated_data, object_serializer):
    validated_data_keys = validated_data.keys()
    required_fields = object_serializer.Meta.required_fields
    check_required_fields = all(
        item in validated_data_keys for item in required_fields)
    if not check_required_fields:
        raise serializers.ValidationError(
            {"required_fields": "You didn't insert all required fields"})
    return True


def default_value(modelname):
    try:
        return modelname.objects.get_or_create(name='Others')[0].id
    except:
        return 1


def default_value_with_value(modelname, code_name):
    try:
        return modelname.objects.get(code_name=code_name).id
    except:
        return uuid.uuid4()


def upload_path_profile(instance, filname):
    # return MEDIA_URL_CLOUD.join(['img', instance.get_type(), instance.user.username, str(instance.created_at), datetime.now().strftime('%H:%M:%S'), filname])
    return MEDIA_URL_CLOUD.join(['img', instance.get_type(), instance.user.username + str(instance.created_at) + datetime.now().strftime('%H:%M:%S'), filname])


def general_update_serializer(original_object, data, context=None):
    object_app = original_object._meta.app_label
    object_name = original_object._meta.object_name
    serializer_module_path = 'apps.' + \
        f'{object_app}.serializers.{object_name}Serializer'
    serializer_class = import_string(serializer_module_path)
    ser = serializer_class(instance=original_object,
                           data=data, partial=True, context=context)
    if ser.is_valid():
        try:
            return ser.update(original_object, ser.validated_data)
        except Exception as e:
            raise serializers.ValidationError(
                {"status": "error", "message": str(e.args)})
    raise serializers.ValidationError(
        {"status": "error", "message": ser.errors})


def general_create_serializer(original_object, data, context=None):
    object_app = original_object._meta.app_label
    object_name = original_object._meta.object_name
    serializer_module_path = 'apps.' + \
        f'{object_app}.serializers.{object_name}Serializer'
    serializer_class = import_string(serializer_module_path)
    ser = serializer_class(data=data, context=context)
    if ser.is_valid():
        return ser.save()
    return None


def validate_start_before_end_date(start_date, end_date):
    if start_date >= end_date:
        raise serializers.ValidationError(
            {"end_date": "End date must be after start date."}
        )


def validate_date_before_today(value):
    today = date.today()
    if value.date() > today:
        raise serializers.ValidationError(
            "the date should be before current date")
    
def validate_date_after_today(value):
    today = date.today()
    if value< today:
        raise serializers.ValidationError(
            "the date should be after current date")


def default_value_user(modelname):
    try:
        return modelname.objects.get_or_create(username='Others', email="dummy@mail.com", password=make_password(''))[0].pk
    except:
        return 1


def upload_path(instance, filname):
    if (instance.get_upload_path() == LOCAL):
       # return MEDIA_URL_LOCAL.join(['img', instance.get_upload_path(), instance.name, str(instance.created_at), datetime.now().strftime('%H:%M:%S'), filname])
        return MEDIA_URL_LOCAL.join(['img', instance.get_upload_path(), instance.get_name + str(instance.created_at) + datetime.now().strftime('%H:%M:%S'), filname])
    else:
        # return MEDIA_URL_CLOUD.join(['img', instance.get_upload_path(), instance.name, str(instance.created_at), datetime.now().strftime('%H:%M:%S'), filname])
        return MEDIA_URL_CLOUD.join(['img', instance.get_upload_path(), instance.get_name + str(instance.created_at) + datetime.now().strftime('%H:%M:%S'), filname])


def upload_path_employee(instance, filname):
    if (instance.get_upload_path() == LOCAL):
       # return MEDIA_URL_LOCAL.join(['img', instance.get_upload_path(), instance.name, str(instance.created_at), datetime.now().strftime('%H:%M:%S'), filname])
        return MEDIA_URL_LOCAL.join(['img', instance.get_upload_path(), instance.user_account.username + str(instance.user_account.date_joined) + datetime.now().strftime('%H:%M:%S'), filname])
    else:
        # return MEDIA_URL_CLOUD.join(['img', instance.get_upload_path(), instance.name, str(instance.created_at), datetime.now().strftime('%H:%M:%S'), filname])
        return MEDIA_URL_CLOUD.join(['img', instance.get_upload_path(), instance.user_account.username + str(instance.user_account.date_joined) + datetime.now().strftime('%H:%M:%S'), filname])


def upload_path_video(instance, filname):
    if (instance.get_upload_path() == LOCAL):
        # return MEDIA_URL_LOCAL.join(['video', instance.get_upload_path(), instance.name, str(instance.created_at), datetime.now().strftime('%H:%M:%S'), filname])
        return MEDIA_URL_LOCAL.join(['video', instance.get_upload_path(), instance.get_name + str(instance.created_at) + datetime.now().strftime('%H:%M:%S'), filname])
    else:
        # return MEDIA_URL_CLOUD.join(['video', instance.get_upload_path(), instance.name, str(instance.created_at), datetime.now().strftime('%H:%M:%S'), filname])
        return MEDIA_URL_CLOUD.join(['video', instance.get_upload_path(), instance.get_name + str(instance.created_at) + datetime.now().strftime('%H:%M:%S'), filname])


def upload_path_file(instance, filname):
    if (instance.get_upload_path() == LOCAL):
        # return MEDIA_URL_LOCAL.join(['files', instance.get_upload_path(), instance.name, str(instance.created_at), datetime.now().strftime('%H:%M:%S'), filname])
        return MEDIA_URL_LOCAL.join(['files', instance.get_upload_path(), instance.get_name + str(instance.created_at) + datetime.now().strftime('%H:%M:%S'), filname])
    else:
        # return MEDIA_URL_CLOUD.join(['files', instance.get_upload_path(), instance.name, str(instance.created_at), datetime.now().strftime('%H:%M:%S'), filname])
        return MEDIA_URL_CLOUD.join(['files', instance.get_upload_path(), instance.get_name + str(instance.created_at) + datetime.now().strftime('%H:%M:%S'), filname])


def general_update_two_objects(instance, source_instance, exclude,):
    dest_fields = instance._meta.fields
    source_fields = source_instance._meta.fields
    dest_fields_name = [field.name for field in dest_fields]
    source_fields_name = [field.name for field in source_fields]

    for field_name in dest_fields_name:
        if field_name in exclude:
            continue
        if field_name in source_fields_name:
            exec("instance.%s = source_instance.%s" %
                 (field_name, field_name))

    instance.save()
    return instance


# def general_update(instance, validated_data, exclude, foreign_fields):
#     fields = instance._meta.fields
#     fields_name = [field.name for field in fields]
#     for key, value in validated_data.items():

#         if key in exclude:
#             continue
#         if key in foreign_fields:
#             field = validated_data.get(key, None)
#             if field:
#                 if type(field.id) == uuid.UUID:
#                     exec("instance.%s = type(instance.%s).objects.get(pk=uuid.UUID('%s'))" %
#                          (key, key, field.id))
#                 else:
#                     exec("instance.%s = type(instance.%s).objects.get(pk=%s)" %
#                          (key, key, field.id))
#                 # exec("instance.%s = field_class.objects.get(pk=%s)" %(field, field_id))

#         elif key in fields_name:
#             if type(value) == str or type(value) == date:
#                 exec("instance.%s = '%s'" %
#                      (key, value))
#             else:
#                 exec("instance.%s = %s" %
#                      (key, value))
#         elif key not in fields_name:
#             exec("instance.%s.set(%s)" %
#                  (key, value))
#     instance.save()
#     return instance

def general_update(instance, validated_data):
    instance_model = type(instance)
    for key, value in validated_data.items():

        model_field = instance_model._meta.get_field(key)
        model_field_type_name = type(model_field).__name__

        if model_field_type_name in ['ManyToManyField']:
            exec("instance.%s.set(%s)" % (key, [str(v.id) for v in value]))
            # exec("instance."+key+".set("+str([v.id for v in value])+")")# % (key, list(value)))
        else:
            setattr(instance, key, value)
        # else:
        #     field = validated_data.get(key, None)
        #     setattr(instance,key, value)
        #     if field:
        #         if type(field.id) == uuid.UUID:
        #             exec("instance.%s = type(instance.%s).objects.get(pk=uuid.UUID('%s'))" %
        #                  (key, key, field.id))
        #         else:
        #             exec("instance.%s = type(instance.%s).objects.get(pk=%s)" %
        #                  (key, key, field.id))
        #         # exec("instance.%s = field_class.objects.get(pk=%s)" %(field, field_id))

        # elif key in fields_name:
        #     if type(value) == str or type(value) == date:
        #         exec("instance.%s = '%s'" %
        #              (key, value))
        #     else:
        #         exec("instance.%s = %s" %
        #              (key, value))
        # elif key not in fields_name:
        #     exec("instance.%s.set(%s)" %
        #          (key, value))
    instance.save()
    return instance


def clone(self):
    new_kwargs = dict([(fld.name, getattr(self, fld.name))
                      for fld in self._meta.fields if fld.name != self._meta.pk])
    new_kwargs.pop('id')
    return self.__class__.objects.create(**new_kwargs)


def check_employee_task_allowance(employee, data, method=None, model=None,  no_task=False):
    try:
        # if the user is employee we should check if the task id the user sent is belong to him/her(the task assigne to him/her)
        # and the task status should be (open, rejected,Uncomplete)
        task_type = None
        task_object = None
        if not no_task:
            try:
                task_id = data['task_id']
            except:
                raise Exception("You should have task to do this action")
            try:
                task = employee.tasks.prefetch_related('content_object', 'task_type__ph_industry').get(
                    pk=task_id, task_status__code_name__in=('Op', 'Rj', 'Uc'))
                task_type = task.task_type
                task_object = task.content_object
            except Exception as e:
                # return CustomResponse(succeeded=False, message="You don't have Open, rejected, or Uncomplete task to do this action", data={}, status=status.HTTP_403_FORBIDDEN)
                raise Exception(
                    "You don't have Open, rejected, or Uncomplete task to do this action " + str(e.args))
        else:
            # app_label = model._meta.app_label
            # model_name = model.__name__
            try:
                active_contract = employee.active_contract
                task_type = active_contract.allowed_task.get(action__request_method__icontains=method.lower(
                ), object_type=ContentType.objects.get_for_model(model))
            # task_type=employee.employee_type.allowed_task_have.get(action__request_method__icontains=method.lower(
            # ), object_type=ContentType.objects.get(app_label=app_label, model=model_name))
            except:
                raise Exception(
                    "You don't have active contract, or youo can't do this task")

        if task_type:
            # if the task need art_category, working country, sub lang we should check if the employee is allowed to work
            # according to these conditions, so we check if the employee has Active contract with these conditions
            if task_type.need_category:
                try:
                    art_category_id = data['category']
                except:
                    if task_object:
                        art_category_id = task_object.category.id
                    else:
                        raise Exception(
                            "You should insert the art category")
                try:
                    active_contract.art_category.get(id=art_category_id)
                except:
                    raise Exception(
                        "You should have the category in your active contract")

            if task_type.need_working_country:
                try:
                    working_country_id = data['main_country']
                except:
                    if task_object:
                        working_country_id = task_object.main_country.id
                    else:
                        raise Exception(
                            "You should insert the main country")
                try:
                    active_contract.working_country.get(id=working_country_id)
                except:
                    raise Exception(
                        "You should be allowed to work in this country in your active contract")

            if task_type.need_sub_language:
                try:
                    sub_language_id = data['main_sub_language']
                except:
                    if task_object:
                        sub_language_id = task_object.main_sub_language.id
                    else:
                        raise Exception(
                            "You should insert the main sub language")
                try:
                    active_contract.sub_l_can_write.get(
                        destination_language__id=sub_language_id)
                except:
                    raise Exception(
                        "You should be allowed to work with this sub language in your active contract")

            if task_type.need_language:
                try:
                    language_id = data['main_language']
                except:
                    if task_object:
                        language_id = task_object.main_language.id
                    else:
                        raise Exception(
                            "You should insert the main language")
                try:
                    active_contract.can_write.get(
                        destination_language__id=language_id)
                except:
                    raise Exception(
                        "You should be allowed to work with this sub language in your active contract")

            try:
                task_object_industry = task_object.ph_type.industry.all()
                task_object_industry_set = {
                    a.code_name for a in task_object_industry}
            except:
                task_object_industry = None
                task_object_industry_set = set()
            try:
                task_ph_industry = task_type.ph_industry.all()
                task_ph_industry_set = {a.code_name for a in task_ph_industry}
            except:
                task_ph_industry = None
                task_ph_industry_set = set()
            try:
                employee_ph_industry = employee.employee_type.ph_industry.all()
                employee_ph_industry_set = {
                    a.code_name for a in employee_ph_industry}
            except:
                employee_ph_industry = None
                employee_ph_industry_set = set()

            if no_task:
                common_industry = task_ph_industry_set & employee_ph_industry_set
                if common_industry:
                    return True
            else:
                common_industry = task_object_industry_set & task_ph_industry_set & employee_ph_industry_set
                if common_industry:
                    return task

            raise Exception(
                "You can not do this task" + str(e.args))
        else:
            raise Exception(
                "You can not do this task" + str(e.args))
    except Exception as e:
        raise Exception("Something wrong happened: "+str(e.args))


def check_payment(user):
    if user == 1:
        return True
    else:
        return False
