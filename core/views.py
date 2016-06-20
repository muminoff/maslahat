from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.algoliasearch import get_adapter

from .models import Post


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def instant_search(request):
    context = {
        'appID': settings.ALGOLIA['APPLICATION_ID'],
        'searchKey': settings.ALGOLIA['SEARCH_API_KEY'],
        'indexName': get_adapter(Post).index_name
    }
    return render(request, 'instant_search.html', context)
