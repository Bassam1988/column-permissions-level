from django.urls import path, include
from apps.classes.GeneralAPIFunctions import GeneralAPI
from rest_framework.routers import DefaultRouter

from .api import EmailTemplateViewSet

app_name = 'custom_email'


general_api_router = DefaultRouter()
general_api_router.register(r'general-detail', GeneralAPI, basename='general-detail')

email_templates_router = DefaultRouter()
email_templates_router.register(r'email_templates', EmailTemplateViewSet, basename='email_template')



urlpatterns = [
               path('', include(email_templates_router.urls)),
               path('', include(general_api_router.urls)),
              
]