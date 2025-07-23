from django.shortcuts import render
from django.http import HttpResponse

def hello(request):
    return HttpResponse("<h1>Hello Django !<h1>")
# Create your views here.

def about(request):
    return HttpResponse("About us")