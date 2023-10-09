from datetime import timedelta
import email


from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


from apps.accounts.models.models import UserModel

from .models import AUTH_USER_MODEL, get_password_reset_token_expiry_time
from . import models

__all__ = [
    'EmailSerializer',
    'PasswordTokenSerializer',
    'ResetTokenSerializer',
]


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordValidateMixin:
    def validate(self, data):
        token = data.get('token')
        email=data.get('email')
        try:
            user=UserModel.objects.get(email=email)
        except:
            raise serializers.ValidationError({"error":_("The e-mail entered is not valid. Please check and try again.")})

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        try:
            reset_password_token = _get_object_or_404(models.ResetPasswordToken, key=token,user=user)
        except (TypeError, ValueError, ValidationError, Http404,
                models.ResetPasswordToken.DoesNotExist):
            raise Http404(_("The OTP password entered is not valid. Please check and try again."))

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(
            hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            raise Http404(_("The token has expired"))
        return data


class PasswordTokenSerializer(PasswordValidateMixin, serializers.Serializer):
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})
    token = serializers.CharField()
    email = serializers.CharField()


class ResetTokenSerializer(PasswordValidateMixin, serializers.Serializer):
    token = serializers.CharField()
