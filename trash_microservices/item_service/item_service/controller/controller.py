from django.http import JsonResponse

from item_service.controller.validators import validate_http_method

class Controller:
    def __init__(self, service):
        self.service = service

    def home(self, request):
        validate_http_method(request, ['GET'])

        res = self.service.home(request)
        return JsonResponse(res)

    def add(self, request):
        validate_http_method(request, ['POST'])

        res = self.service.add(request)
        return JsonResponse(res)