from rest_framework import serializers


from .models import *



class EmailTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailTemplate
        fields = ['template_key', 'subject',
                  'body_1', 'body_2', 'body_3']


