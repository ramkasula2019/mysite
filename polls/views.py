from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index (requests):
    return HttpResponse("Hello world, this is django initiation tutorial")

