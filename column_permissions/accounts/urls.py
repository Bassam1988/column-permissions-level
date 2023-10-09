from django.urls import path, include

from classes.GeneralAPIFunctions import GeneralAPI
from .apis.users_api import RegisterAPI, LoginAPI, UserAPI,  ChangePasswordView, SendPasswordCode
from .apis.custom_authorizations_api import PermissionActionViewSet, ContentTypeViewSet, CustomPermissionViewSet, CustomGroupViewSet
from knox import views as knox_views
from rest_framework.routers import DefaultRouter

app_name = 'accounts'


general_api_router = DefaultRouter()
general_api_router.register(r'general', GeneralAPI, basename='general')

permission_action_router = DefaultRouter()
permission_action_router.register(
    r'permission_actions', PermissionActionViewSet, basename='permission_action')

content_type_router = DefaultRouter()
content_type_router.register(
    r'content_types', ContentTypeViewSet, basename='content_type')

custom_permission_router = DefaultRouter()
custom_permission_router.register(
    r'custom_permissions', CustomPermissionViewSet, basename='custom_permission')

custom_group_router = DefaultRouter()
custom_group_router.register(
    r'custom_groups', CustomGroupViewSet, basename='custom_group')

urlpatterns = [
    # path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view()),

    path('api/auth/logout', knox_views.LogoutView.as_view(), name="knox_logout"),
    path('api/auth/logoutall', knox_views.LogoutAllView.as_view(),
         name="knox_logout_all"),

    path('api/auth/change-password',
         ChangePasswordView.as_view(), name='change-password'),
    path('api/auth/send_code', SendPasswordCode.as_view()),
    path('api/auth/password_reset/',
         include('apps.pediahome_resetpassword.urls', namespace='password_reset')),

    path('', include(permission_action_router.urls)),
    path('', include(content_type_router.urls)),
    path('', include(custom_permission_router.urls)),
    path('', include(custom_group_router.urls)),
    path('',include(general_api_router.urls)),
]
