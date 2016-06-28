# Django
import django
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.db import connection
from django.db.models import Count, Sum
from django.db.models.functions import TruncYear, TruncMonth, ExtractWeekDay

# Core
from .models import Post

# Misc
import redis
import sys
import os
from urllib.parse import urlparse
redis_url = urlparse(os.environ.get('REDIS_URL'))

# Stathat
from stathat import StatHat


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
                angrys=Sum('angrys')).order_by('-year')
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
                angrys=Sum('angrys')).order_by('month')
    }
    return render(request, 'stat_monthly.html', context)


def stat_weekdays(request):
    context = {
        'posts_per_weekday': Post.objects.annotate(
            weekday=ExtractWeekDay('published')).values('weekday').annotate(
                posts=Count('id'),
                comments=Sum('comments'),
                reactions=Sum('reactions'),
                shares=Sum('shares'),
                likes=Sum('likes'),
                loves=Sum('loves'),
                wows=Sum('wows'),
                hahas=Sum('hahas'),
                sads=Sum('sads'),
                angrys=Sum('angrys')).order_by('weekday')
    }
    return render(request, 'stat_weekdays.html', context)


def top_posters(request):
    context = {
        'top_posters': Post.objects.values('author', 'author_id').annotate(
            times=Count('author'),
            comments=Sum('comments'),
            reactions=Sum('reactions'),
            shares=Sum('shares'),
            likes=Sum('likes'),
            loves=Sum('loves'),
            wows=Sum('wows'),
            hahas=Sum('hahas'),
            sads=Sum('sads'),
            angrys=Sum('angrys')).order_by('-times')[:20]
    }
    return render(request, 'top_posters.html', context)


def top_shared_posts(request):
    context = {
        'top_shared_posts': Post.objects.order_by('-shares')[:20]
    }
    return render(request, 'top_shared_posts.html', context)


def top_commented_posts(request):
    context = {
        'top_commented_posts': Post.objects.order_by('-comments')[:20]
    }
    return render(request, 'top_commented_posts.html', context)


def top_liked_posts(request):
    context = {
        'top_liked_posts': Post.objects.order_by('-likes')[:20]
    }
    return render(request, 'top_liked_posts.html', context)


def index(request):
    stats = StatHat(settings.STATHAT_ACCOUNT)
    stats.count('user.visited', 1)
    return render(request, 'index.html')


def feed(request):
    context = {
        'new_posts': Post.objects.order_by('-published')[:10]
    }
    return render(request, 'feed.html', context)


def about(request):
    context = {
        'python_version': get_python_version(),
        'django_version': django.get_version(),
        'postgre_version': get_postgre_version(),
        'redis_version': get_redis_version(),
    }
    return render(request, 'about.html', context)


def search(request):
    text = request.GET.get('text')
    results = Post.objects.all()

    if text:
        results = Post.objects.filter(
            text__icontains=text
            ).order_by('-published')
    else:
        results = None
    context = { 'results': results, 'text': text }
    return render(request, 'search.html', context)


def author_posts(request, author):
    context = {
        'posts': Post.objects.filter(author=author).order_by('-published'),
        'author': author
    }
    return render(request, 'author_posts.html', context)

def group_facts(request):
    cursor = connection.cursor()
    cursor.execute("""
    select
      month,
      (total::float / lag(total) over (order by month) - 1) * 100 growth
      from (
        select to_char(published, 'yyyy-mm') as month,
        count(shares) total
        from core_post
        group by month
      ) s
      order by month;
    """)
    result = cursor.fetchone()[0]
    context = {
        'group_facts': result
    }
    return render(request, 'group_facts.html', context)

def facts():
    cursor = connection.cursor()
    cursor.execute("""
    select
      month,
      (total::float / lag(total) over (order by month) - 1) * 100 growth
      from (
        select to_char(published, 'yyyy-mm') as month,
        count(shares) total
        from core_post
        group by month
      ) s
      order by month;
    """)
    return cursor.fetchall()


def not_found(request):
    return render(request, '404.html')


def server_error(request):
    return render(request, '500.html')

def get_python_version():
    return sys.version

def get_postgre_version():
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    return cursor.fetchone()[0]

def get_redis_version():
    r = redis.StrictRedis(
        host=redis_url.hostname,
        port=redis_url.port,
        db=0,
        password=redis_url.password)
    return r.info()['redis_version']
