import uuid
from django.db import models

from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.urls import reverse

import string


class EmailTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template_key = models.CharField(max_length=75, unique=True)
    subject = models.CharField(max_length=200)
    body_1 = models.CharField(max_length=500)
    body_2 = models.CharField(max_length=500, blank=True)
    body_3 = models.CharField(max_length=500, blank=True)
    from_email = models.EmailField(default='pediahome@pediahome.com')
    description = models.CharField(max_length=500, default="")


def send_custom_email(object, template_key, manual_text=None):
    email_template = EmailTemplate.objects.get(template_key=template_key)
    to_email = None
    subject = email_template.subject
    from_email = email_template.from_email
    if template_key == 'CtPEABE':
        user = object.pedia_account.user
        to_email = user.email
        alphabet = string.ascii_letters + string.digits+'_$'
        password = get_random_string(length=10, allowed_chars=alphabet)+"_300"
        user.set_password(password)
        user.save()

        dear_part = "Dear " + object.name + "\n"
        body = email_template.body_1+"\n"

        if email_template.body_2:
            body += email_template.body_2+"\n"
        if email_template.body_3:
            body = email_template.body_3+"\n"

        user_pass = "username: "+to_email + "\n"
        user_pass += "Password: "+password + "\n"
        complete_message = dear_part+body+user_pass

    elif template_key == 'CtDEABE':
        user = object.pedia_account.user
        to_email = user.ph_emails.get(
            industry__code_name='DW', status__code_name='At')
        alphabet = string.ascii_letters + string.digits+'_$'
        password = get_random_string(length=10, allowed_chars=alphabet)+"_300"
        user.set_password(password)
        user.save()

        dear_part = "Dear " + object.name + "\n"
        body = email_template.body_1+"\n"

        if email_template.body_2:
            body += email_template.body_2+"\n"
        if email_template.body_3:
            body = email_template.body_3+"\n"

        user_pass = "username: "+to_email + "\n"
        user_pass += "Password: "+password + "\n"
        complete_message = dear_part+body+user_pass

    elif template_key == 'CtDEPAS':

        to_email = object.pedia_account.user.ph_emails.get(
            industry__code_name='DW', status__code_name='At')
        dear_part = "Dear " + object.name + "\n"
        body = email_template.body_1+"\n"

        if email_template.body_2:
            body += email_template.body_2+"\n"
        if email_template.body_3:
            body = email_template.body_3+"\n"
        complete_message = dear_part+body

    elif template_key == 'CtDEPFS':

        to_email = object.entity_mail
        dear_part = "Dear " + object.name + "\n"
        body = email_template.body_1+"\n"

        if email_template.body_2:
            body += email_template.body_2+"\n"
        if email_template.body_3:
            body = email_template.body_3+"\n"
        complete_message = dear_part+body

    elif template_key == 'CtDEPR':

        to_email = object.pedia_account.user.ph_emails.get(
            industry__code_name='DW', status__code_name='At')
        dear_part = "Dear " + object.name + "\n"
        body = email_template.body_1+"\n"

        if email_template.body_2:
            body += email_template.body_2+"\n"
        if email_template.body_3:
            body += email_template.body_3+"\n"
        if manual_text:
            body += manual_text+"\n"

        complete_message = dear_part+body

    elif template_key == 'CtRP':
        user = object.user
        to_email = user.email
        key = object.key

        email_plaintext_message = "{}?token={}".format(
            reverse('password_reset:reset-password-request'), key)

        dear_part = "Dear " + user.first_name + "\n"
        body = email_template.body_1+"\n"

        if email_template.body_2:
            body += email_template.body_2+"\n"
        if email_template.body_3:
            body = email_template.body_3+"\n"

        complete_message = dear_part+body+email_plaintext_message

    # This email will be sent when an employee create new pediahome account for new user, CtDTABE: Create DobbiWood Talent Account By Employee
    elif template_key == 'CtDTABE':
        user = object.pedia_account.user
        to_email = user.email
        alphabet = string.ascii_letters + string.digits+'_$'
        password = get_random_string(length=10, allowed_chars=alphabet)+"_300"
        user.set_password(password)
        user.save()

        dear_part = "Dear " + object.name + "\n"
        body = email_template.body_1+"\n"

        if email_template.body_2:
            body += email_template.body_2+"\n"
        if email_template.body_3:
            body = email_template.body_3+"\n"

        user_pass = "username: "+to_email + "\n"
        user_pass += "Password: "+password + "\n"
        complete_message = dear_part+body+user_pass

    # This email will be sent when an employee create new pediahome account for new user, CtDSABE: Create DubbiWood Specialist Account By Employee
    elif template_key == 'CtDSABE':
        user = object.pedia_account.user
        to_email = user.email
        alphabet = string.ascii_letters + string.digits+'_$'
        password = get_random_string(length=10, allowed_chars=alphabet)+"_300"
        user.set_password(password)
        user.save()

        dear_part = "Dear " + object.name + "\n"
        body = email_template.body_1+"\n"

        if email_template.body_2:
            body += email_template.body_2+"\n"
        if email_template.body_3:
            body = email_template.body_3+"\n"

        user_pass = "username: "+to_email + "\n"
        user_pass += "Password: "+password + "\n"
        complete_message = dear_part+body+user_pass

    send_mail(
        # title:
        subject,
        # message:
        complete_message,
        # from:
        from_email,
        # to:
        [to_email]
    )


"""
def send_pr_entity_notification_email(entity, template_key):
    email_template = EmailTemplate.objects.get(template_key=template_key)
    # email_template_data=EmailTemplateSerializer(email_template).data
    user = entity.pedia_account.user
    to_email = user.email

    from_email = email_template.from_email
    if template_key == 'CtPEABE':
        alphabet = string.ascii_letters + string.digits+'_$'
        password = get_random_string(length=10, allowed_chars=alphabet)+"_300"
        user.set_password(password)
        user.save()
        subject = email_template.subject
        dear_part = "Dear " + entity.name + "\n"
        body = email_template.body_1+"\n"

        if email_template.body_2:
            body += email_template.body_2+"\n"
        if email_template.body_3:
            body = email_template.body_3+"\n"

        user_pass = "username: "+to_email + "\n"
        user_pass += "Password: "+password + "\n"
        complete_message = dear_part+body+user_pass
    send_mail(
        # title:
        subject,
        # message:
        complete_message,
        # from:
        from_email,
        # to:
        [to_email]
    )


def send_reset_password_token_notification_email(reset_password_token, template_key):
    email_template = EmailTemplate.objects.get(template_key=template_key)
    # email_template_data=EmailTemplateSerializer(email_template).data
    
    subject = email_template.subject
    from_email = email_template.from_email
    if template_key == 'CtRP':
        user = reset_password_token.user
        to_email = user.email
        key = reset_password_token.key

        email_plaintext_message = "{}?token={}".format(
            reverse('password_reset:reset-password-request'), key)

        dear_part = "Dear " + user.first_name + "\n"
        body = email_template.body_1+"\n"

        if email_template.body_2:
            body += email_template.body_2+"\n"
        if email_template.body_3:
            body = email_template.body_3+"\n"

       
        complete_message = dear_part+body+email_plaintext_message
        
    send_mail(
        # title:
        subject ,
        # message:
        complete_message,
        # from:
        from_email,
        # to:
        to_email
    )


def send_dw_entity_notification_email(entity, template_key):
    email_template = EmailTemplate.objects.get(template_key=template_key)
    # email_template_data=EmailTemplateSerializer(email_template).data
    user = entity.pedia_account.user
    to_email = user.email
    subject = email_template.subject
    from_email = email_template.from_email

    if template_key == 'CtDEPAS':
        pass
    
    send_mail(
        # title:
        subject ,
        # message:
        complete_message,
        # from:
        from_email,
        # to:
        to_email
    )
"""
