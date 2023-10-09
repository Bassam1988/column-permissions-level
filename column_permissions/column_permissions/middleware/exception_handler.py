from classes.CustomResponse import CustomResponse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied


class ExceptionHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, AuthenticationFailed):
            response_data = 'error: Authentication failed. details:' + \
                str(exception)

        elif isinstance(exception, PermissionDenied):
            response_data = 'error: Permission denied.details:' + \
                str(exception)

        else:
            response_data = "error: " + str(
                exception.args)
        response = CustomResponse(succeeded=False, message=response_data, data={
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        return response
