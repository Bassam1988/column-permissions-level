from rest_framework import status
from rest_framework.response import Response


class CustomResponse(Response):
    response_data = {
        "succeeded": True,
        "message": "",
        "data": {}
    }
    status = status.HTTP_200_OK

    def __init__(self, succeeded=None, message=None, data=None, status=None, *args, **kwargs):

        if succeeded != None:
            self.response_data["succeeded"] = succeeded

        if message != None:
            self.response_data["message"] = message

        if data != None:
            self.response_data["data"] = data

        if status != None:
            self.status = status

        kwargs['data'] = self.response_data
        kwargs['status'] = self.status

        super(
            CustomResponse, self).__init__(*args, **kwargs)
