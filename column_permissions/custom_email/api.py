
from rest_framework import viewsets, permissions

from .models import EmailTemplate

from .serializers import EmailTemplateSerializer


class EmailTemplateViewSet(viewsets.ModelViewSet):
    #queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or (hasattr(user, 'pediahome_employee') and user.pediahome_employee.employee_type.code_name == 'PH_A'):
            return EmailTemplate.objects.all()

        return EmailTemplate.objects.none()
