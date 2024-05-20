from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse("Main page")

def search(request):
    if request.method == "GET":
        query = request.GET.get('q','')
    return HttpResponse("Search page")

def user(request, uid):
    return HttpResponse("User page")