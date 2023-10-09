from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from knox.models import AuthToken
from ..serializers.user_serializers import UserSerializer, RegisterSerializer, LoginSerializer,\
    ChangePasswordSerializer, ChangePasswordCodeSerializer
from ..models.models import UserModel

from apps.classes.CustomResponse import CustomResponse

"""
class IsCreationOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_superuser:
            if view.action == 'list' or view.action == 'retrieve':
                return True
            else:
                return False
        else:
            return True

"""
# Register API


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            data = {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": (AuthToken.objects.create(user))[1]}
            CustomResponse(succeeded=True, message="", data=data,
                           status=status.HTTP_201_CREATED)
        else:
            CustomResponse(succeeded=False, message=serializer.errors,
                           data={}, status=status.HTTP_400_BAD_REQUEST)


# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        user = serializer.login(data=request.data)
        if user:
            data = {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1]}
            return CustomResponse(succeeded=True, message="", data=data)
                
        #else:
                #return CustomResponse(succeeded=False, message=serializer.errors, data={}, status=status.HTTP_400_BAD_REQUEST)
                
        
# Get User API


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class SendPasswordCode(generics.GenericAPIView):
    serializer_class = ChangePasswordCodeSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        data = {'user': request.user.id}

        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            confirmation_code = serializer.data

            subject = 'Change Password Confirmation Code'
            body = 'confirmation code is: ' + confirmation_code['code']
            from_email = 'pediahome@pediahome.com'
            to_emial = [request.user.email]
            send_mail(
                subject,
                body,
                from_email,
                to_emial,
                fail_silently=False,
            )
            return CustomResponse(succeeded=True, message='Confirmation code was sent successfully', data={}, status=status.HTTP_201_CREATED)

        CustomResponse(succeeded=False, message='Please try again later', data={
        }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = UserModel
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(
            instance=user, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                serializer.save()
                return CustomResponse(succeeded=True, message='Password updated successfully', data={}, status=status.HTTP_200_OK)
            except Exception as e:
                return CustomResponse(succeeded=False, message='please try again: ' + str(e.args), data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return CustomResponse(succeeded=False, message=serializer.errors, data={}, status=status.HTTP_400_BAD_REQUEST)
