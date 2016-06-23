from django.conf.urls import (
    include, url, handler400, handler403, handler404, handler500)

import core.views

urlpatterns = [
    url(r'^$', core.views.index, name='index'),
    url(r'^feed/$', core.views.feed, name='feed'),
    url(r'^about/$', core.views.about, name='about'),
    url(r'^search/$', core.views.search, name='search'),
    url(r'^stat/yearly/$', core.views.stat_yearly, name='stat_yearly'),
    url(r'^stat/monthly/$', core.views.stat_monthly, name='stat_monthly'),
    url(r'^stat/weekdays/$', core.views.stat_weekdays, name='stat_weekdays'),
    url(r'^top/posters/$', core.views.top_posters, name='top_posters'),
    url(r'^top/shared/posts/$', core.views.top_shared_posts, name='top_shared_posts'),
    url(r'^top/commented/posts/$', core.views.top_commented_posts, name='top_commented_posts'),
]

handler404 = 'core.views.not_found'
handler500 = 'core.views.server_error'
