# Django
import django
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.db import connection
from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncYear, TruncMonth, ExtractWeekDay
from django.views.generic import TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Core
from .models import Post

# Misc
import redis
import sys
import os
import pickle
from urllib.parse import urlparse
redis_url = urlparse(os.environ.get('REDIS_URL'))
import itertools
import time

# Stathat
from stathat import StatHat

# Hashids
from hashids import Hashids


class LastPostsView(TemplateView):
    template_name = 'last_posts.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LastPostsView, self).get_context_data(*args, **kwargs)
        context['last_posts'] = Post.objects.order_by('-published')[:20]
        return context


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
            angrys=Sum('angrys')).order_by('-times')[:50]
    }
    return render(request, 'top_posters.html', context)


def top_shared_posts(request):
    context = {
        'top_shared_posts': Post.objects.order_by('-shares')[:50]
    }
    return render(request, 'top_shared_posts.html', context)


def top_commented_posts(request):
    context = {
        'top_commented_posts': Post.objects.order_by('-comments')[:50]
    }
    return render(request, 'top_commented_posts.html', context)


def top_liked_posts(request):
    context = {
        'top_liked_posts': Post.objects.order_by('-likes')[:50]
    }
    return render(request, 'top_liked_posts.html', context)


def login(request):
    return render(request, 'login.html')


def about(request):
    context = {
        'os_info': get_os_info(),
        'python_version': get_python_version(),
        'django_version': django.get_version(),
        'postgres_version': get_postgres_version(),
        'redis_version': get_redis_version(),
        'last_updated': pickle.loads(get_last_updated()),
    }
    return render(request, 'about.html', context)


class SearchView(TemplateView):
    template_name = 'search.html'
    paginate_by = getattr(settings, 'DEFAULT_PAGINATE_BY', 10)

    def get(self, request, *args, **kwargs):
        self.results = list()
        self.took = 0
        q = request.GET.get('q')

        if q:
            q = q.strip()
            start_time = time.time()
            self.results = Post.objects.filter(
                Q(text__icontains=q) |
                Q(author__icontains=q)).order_by('-published')
            self.took = round(time.time() - start_time, 4)

        paginator = Paginator(self.results, self.paginate_by)
        page = request.GET.get('page', 1)

        try:
            self.results = paginator.page(page)
        except PageNotAnInteger:
            self.results = paginator.page(1)
        except EmptyPage:
            self.results = paginator.page(paginator.num_pages)

        return super(SearchView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context['results'] = self.results
        context['took'] = self.took
        return context


def author_posts(request, hashid):
    hashids = Hashids(salt=settings.SECRET_KEY)
    author_id = hashids.decode(str(hashid))[0]
    context = {
        'posts': Post.objects.filter(
            author_id=author_id).order_by('-published'),
        'author': Post.objects.filter(author_id=author_id)[0].author,
        'author_id': author_id,
    }
    return render(request, 'author_posts.html', context)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def group_growth(request):
    import psycopg2
    cursor = connection.cursor()

    cursor.execute("""
    select month, mmonth, yyear, sum(total_reactions) over (order by yyear, mmonth) as reactions from (
	select month, mmonth, yyear, total_reactions
	from (
	    select to_char(published, 'mm-yyyy') as month,
	    extract(year from published) as yyear,
	    extract(month from published) as mmonth,
	    sum(reactions) total_reactions
	    from core_post
	    group by month, yyear, mmonth
	    order by yyear asc, mmonth asc
	) s
    ) reactions_growth;
    """)
    reactions_facts = dictfetchall(cursor)

    cursor.execute("""
    select month, mmonth, yyear, sum(total_comments) over (order by yyear, mmonth) as comments from (
	select month, mmonth, yyear, total_comments
	from (
	    select to_char(published, 'mm-yyyy') as month,
	    extract(year from published) as yyear,
	    extract(month from published) as mmonth,
	    sum(comments) total_comments
	    from core_post
	    group by month, yyear, mmonth
	    order by yyear asc, mmonth asc
	) s
    ) comments_growth;
    """)
    comments_facts = dictfetchall(cursor)

    cursor.execute("""
    select month, mmonth, yyear, sum(total_shares) over (order by yyear, mmonth) as shares from (
	select month, mmonth, yyear, total_shares
	from (
	    select to_char(published, 'mm-yyyy') as month,
	    extract(year from published) as yyear,
	    extract(month from published) as mmonth,
	    sum(shares) total_shares
	    from core_post
	    group by month, yyear, mmonth
	    order by yyear asc, mmonth asc
	) s
    ) shares_growth;
    """)
    shares_facts = dictfetchall(cursor)

    context = {
        'reactions_facts': reactions_facts,
        'comments_facts': comments_facts,
        'shares_facts': shares_facts
    }
    return render(request, 'group_growth.html', context)


def not_found(request):
    return render(request, '404.html')


def server_error(request):
    return render(request, '500.html')


def get_os_info():
    import platform
    return platform.platform()


def get_python_version():
    return sys.version


def get_postgres_version():
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


def get_last_updated():
    r = redis.StrictRedis(
        host=redis_url.hostname,
        port=redis_url.port,
        db=0,
        password=redis_url.password)
    ret = r.get('last_updated')

    if not ret:
        return pickle.dumps(timezone.now())

    return ret
