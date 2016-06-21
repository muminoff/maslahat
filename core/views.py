from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import Post


def index(request):
    context = {
        'last_posts': Post.objects.order_by('-published')[:100]
    }
    return render(request, 'index.html', context)
