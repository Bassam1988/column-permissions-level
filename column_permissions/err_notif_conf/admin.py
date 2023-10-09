from django.contrib import admin


from .models.models import Status
from .models.configuration_models import Configuration, ConfigurationType
from .models.error_models import ErrorType


admin.site.register(Configuration)

admin.site.register(Status)

admin.site.register(ConfigurationType)

admin.site.register(ErrorType)