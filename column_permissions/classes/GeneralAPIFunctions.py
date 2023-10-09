from django.apps import apps
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from apps.accounts.CustomPermission import PediahomePermission
from apps.classes.CustomResponse import CustomResponse

from rest_framework import status, viewsets, permissions
from .GeneralSerializer import GeneralSerializer


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    """
    Same as Django's standard shortcut, but make sure to also raise 404
    if the filter_kwargs don't match the required types.
    """
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, ValidationError):
        raise Http404


class GeneralAPI(viewsets.ModelViewSet):
    # permission_classes =  [permissions.DjangoModelPermissions,]
    permission_classes = [PediahomePermission]
    lookup_field = 'pk'

    def __init__(self, model=None, serializer=None, *args, **kwargs):

        # try:
        super(GeneralAPI, self).__init__(*args, **kwargs)
        if model:
            self.model = model
        else:
            self.model = None
        if serializer:
            self.serializer_class = serializer
        else:
            self.serializer_class = GeneralSerializer
        # except Exception as e:
        #    return CustomResponse(succeeded=False, message="please try again: "+str(e.args), data={}, status=status.HTTP_400_BAD_REQUEST)

    @property
    def get_model(self):
        return self.model.__name__

    def get_queryset(self):
        if not self.model:
            parm1 = self.kwargs['pk']
            if parm1:
                parm = parm1.split(",")
            app_label = parm[1]
            model_name = parm[2]
            self.model = apps.get_model(
                app_label=app_label, model_name=model_name)

        queryset = self.model.objects.all()
        return queryset

    def get_serializer(self, instance=None, data=None, many=False, partial=False, fields=[], display_fields=[], model=None, *args, **kwargs):
        request = self.request
        kwargs['instance'] = instance
        kwargs['many'] = many
        kwargs['partial'] = partial
        kwargs['fields'] = self.fields
        kwargs['display_fields'] = self.display_fields
        kwargs['context'] = {'request': request}
        if model:
            kwargs['model'] = model

        if data:
            kwargs['data'] = data
        return self.serializer_class(*args, **kwargs)

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        pk = self.kwargs[lookup_url_kwarg]
        parm = pk.split(",")
        pk1 = parm[0]

        filter_kwargs = {self.lookup_field: pk1}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def retrieve(self, request, pk=None):
        parm = pk.split(",")

        try:
            model_name = self.model.__name__
        except:
            model_name = parm[2]

        instance = self.get_object()
        serializer = self.get_serializer(
            instance, model=self.model)
        data = {model_name: serializer.data}
        return CustomResponse(succeeded=True, message='', data=data, status=status.HTTP_200_OK)

    def list(self, request):
        model_name = self.model.__name__
        instances = self.get_queryset()
        serializer = self.get_serializer(
            instances, model=self.model, many=True)
        data = {model_name: serializer.data}
        return CustomResponse(succeeded=True, message="", data=data, status=status.HTTP_200_OK)

    def create(self, request):
        model_name = self.model.__name__
        user = request.user
        if user.is_superuser:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {model_name: serializer.data}
                return CustomResponse(succeeded=True, message='', data=data, status=status.HTTP_200_OK)
            else:
                return CustomResponse(succeeded=False, message=serializer.errors, data={}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return CustomResponse(succeeded=False, message="You don't have permission to perform this action", data={}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        model_name = self.model.__name__
        user = request.user
        if user.is_superuser:
            queryset = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(
                queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {model_name: serializer.data}
                return CustomResponse(succeeded=True, message='', data=data, status=status.HTTP_200_OK)
            else:
                return CustomResponse(succeeded=False, message=serializer.errors, data={}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return CustomResponse(succeeded=False, message="You don't have permission to perform this action", data={}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        model_name = self.model.__name__
        user = request.user
        if user.is_superuser:
            queryset = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(
                queryset, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                data = {model_name: serializer.data}
                return CustomResponse(succeeded=True, message='', data=data, status=status.HTTP_200_OK)
            else:
                return CustomResponse(succeeded=False, message=serializer.errors, data={}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return CustomResponse(succeeded=False, message="You don't have permission to perform this action", data={}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        return CustomResponse(succeeded=False, message="You don't have permission to perform this action", data={}, status=status.HTTP_403_FORBIDDEN)
###################### APIs for static tables ##########################
