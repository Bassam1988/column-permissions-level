import uuid
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.db import models
from django.apps import apps

from .models import Status

from apps.classes.GeneralFunctions import default_value


class NotificationType(models.Model):
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


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.ForeignKey(
        NotificationType, on_delete=models.SET(default_value(NotificationType)))
    name = models.CharField(max_length=50)
    code_name = models.CharField(max_length=10)
    description = models.CharField(max_length=300)
    message_text = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(
        Status, on_delete=models.SET(default_value(Status)))

    @property
    def get_name(self):
        return self.name


class SendingNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification = models.ForeignKey(
        Notification, on_delete=models.SET(default_value(Notification)))
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="noti_sent_by_me")
    object_id = models.CharField(max_length=200)
    from_user = GenericForeignKey('content_type', 'object_id')

    content_type_2 = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="noti_sent_to_me", null=True)
    object_id_2 = models.CharField(max_length=200, blank=True)
    to_user = GenericForeignKey('content_type_2', 'object_id_2')

    content_type_3 = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="noti_first_object")
    object_id_3 = models.CharField(max_length=200)
    content_object_3 = GenericForeignKey('content_type_3', 'object_id_3')

    content_type_4 = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="noti_second_object", null=True)
    object_id_4 = models.CharField(max_length=200, blank=True)
    content_object_4 = GenericForeignKey('content_type_4', 'object_id_4')
    notification_text = models.CharField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def get_name(self):
        return self.from_user.get_name+" -> "+self.to_user.get_name+": "+self.content_object_3.get_name+" -> "+self.content_object_4.get_name

    @classmethod
    def send_notification(cls, parameters, noti_code_name):
        notification = Notification.objects.select_related(
            'type').get(code_name=noti_code_name)
        from_user = parameters['from']
        to_user = parameters['to']
        if notification.type.code_name == 'InUTUNt' and from_user.profile_type.ph_profile_type.code_name != to_user.profile_type.ph_profile_type.code_name:
            raise Exception(
                {"message": "This type of notifications should be between two users in the same industry"})

        if noti_code_name == 'MDADN':
            dubbing_artwork = parameters['dubbing_artwork']
            other_work = parameters['other_work']

            sending_notification = cls(notification=notification, from_user=from_user, to_user=to_user,
                                       content_object_3=dubbing_artwork, content_object_4=other_work, notification_text="")
            sending_notification.save()
            return sending_notification

        if noti_code_name == 'NDAAN':
            dubbing_artwork = parameters['dubbing_artwork']
            other_work = parameters['other_work']

            sending_notification = cls(notification=notification, from_user=from_user, to_user=to_user,
                                       content_object_3=dubbing_artwork, content_object_4=other_work, notification_text="")
            sending_notification.save()
            return sending_notification

        if noti_code_name == 'NDTAN':
            talent_work = parameters['talent_work']
            dubbing_artwork = parameters['dubbing_artwork']

            sending_notification = cls(notification=notification, from_user=from_user, to_user=to_user,
                                       content_object_3=talent_work, content_object_4=dubbing_artwork, notification_text="")
            sending_notification.save()
            return sending_notification
