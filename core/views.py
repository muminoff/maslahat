from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Count, Sum
from django.db.models.functions import TruncYear, TruncMonth
from .models import Post


def stat_yearly(request):
    context = {
        'posts_per_year': Post.objects.annotate(
            year=TruncYear('published')).values('year').annotate(
                posts=Count('id'),
                comments=Sum('comments'),
                reactions=Sum('reactions'),
                shares=Sum('shares'),
                likes=Sum('likes'),
                loves=Sum('loves'),
                wows=Sum('wows'),
                hahas=Sum('hahas'),
                sads=Sum('sads'),
                angrys=Sum('angrys').order_by('-year'))
    }
    return render(request, 'stat_yearly.html', context)


def stat_monthly(request):
    context = {
        'posts_per_month': Post.objects.annotate(
            month=TruncMonth('published')).values('month').annotate(
                posts=Count('id'),
                comments=Sum('comments'),
                reactions=Sum('reactions'),
                shares=Sum('shares'),
                likes=Sum('likes'),
                loves=Sum('loves'),
                wows=Sum('wows'),
                hahas=Sum('hahas'),
                sads=Sum('sads'),
                angrys=Sum('angrys').order_by('-month'))
    }
    return render(request, 'stat_monthly.html', context)


def index(request):
    context = {
        'last_posts': Post.objects.order_by('-published')[:100]
    }
    return render(request, 'index.html', context)
