from django.shortcuts import render
from .models import *


# Create your views here.

def index(request):
    return render(request, 'index.html', locals())


def login(request):
    return render(request, 'index.html', locals())


def logout(request):
    return render(request, 'index.html', locals())


def register(request):
    return render(request, 'index.html', locals())


def forget(request):
    return render(request, 'index.html', locals())
