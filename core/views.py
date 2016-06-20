from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.algoliasearch import get_adapter

from .models import Post


# Create your views here.
def index(request):
    context = {
        'last_posts': Post.objects.order_by('-published').all()[:10]
    }
    return render(request, 'index.html', context)


def instant_search(request):
    context = {
        'appID': settings.ALGOLIA['APPLICATION_ID'],
        'searchKey': settings.ALGOLIA['API_KEY'],
        'indexName': get_adapter(Post).index_name
    }
    return render(request, 'instant_search.html', context)
