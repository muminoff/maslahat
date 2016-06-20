from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.algoliasearch import get_adapter

from .models import Post


def index(request):
    return render(request, 'index.html')
