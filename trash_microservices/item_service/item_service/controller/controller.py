from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

class Controller:
    def __init__(self, service):
        self.service = service

    def home(self, request):
        if request.method != "GET":
            return HttpResponse("Method Not Allowed", status=405)
        res = self.service.home(request)
        return JsonResponse(res)

    def add(self, request):
        if request.method != "POST":
            return HttpResponse("Method Not Allowed", status=405)
        res = self.service.add(request)
        return JsonResponse(res)