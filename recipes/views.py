from django.http import HttpResponse


def home(request):
    return HttpResponse('<html><title>cookbook</title></html>')