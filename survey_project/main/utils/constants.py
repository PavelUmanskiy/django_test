from http import HTTPStatus

from django.http import HttpResponse


class HttpResponseCreated(HttpResponse):
    status_code = HTTPStatus.CREATED