from django.http import HttpResponse

def home(request):
    return HttpResponse("This is homepage")

def about(request):
    return HttpResponse("This is about page")