import uuid

from django.conf import settings
from django.db import models
from django.apps import apps

from .models import Status

from classes.GeneralFunctions import default_value


class ConfigurationType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    code_name = models.CharField(max_length=10)
    description = models.CharField(max_length=300)
    status = models.ForeignKey(
        Status, on_delete=models.SET(default_value(Status)))
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def get_name(self):
        return self.name


class Configuration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.ForeignKey(
        ConfigurationType, on_delete=models.SET(default_value(ConfigurationType)))
    name = models.CharField(max_length=100)
    default_value_name = models.CharField(max_length=150)
    code_name = models.CharField(max_length=10)
    description = models.CharField(max_length=400)
    value = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(
        Status, on_delete=models.SET(default_value(Status)))

    @property
    def get_name(self):
        return self.name


def get_config_parm_value(code_name):
    err_notif_conf_app = getattr(settings, 'ERR_NOTIF_CONF_APP')
    configuration_model = getattr(settings, 'CONFIGURATION_MODEL')
    try:
        config_parm = apps.get_model(err_notif_conf_app, configuration_model).objects.get(
            code_name=code_name, status__code_name='At')
        config_parm_value = config_parm.value
    except:
        default_value_name = apps.get_model(err_notif_conf_app, configuration_model).objects.get(
            code_name=code_name).default_value_name
        config_parm_value = getattr(settings, default_value_name)

    return config_parm_value