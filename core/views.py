from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import Post


def index(request):
    return render(request, 'index.html')
