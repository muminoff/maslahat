from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf.urls import (
    include, url, handler400, handler403, handler404, handler500)

import core.views

urlpatterns = [
    url(r'^maslahat/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^login/$', core.views.login, name='login'),
    url(r'^latest/$', login_required(core.views.LastPostsView.as_view()), name='latest'),
    url(r'^about/$', login_required(core.views.about), name='about'),
    url(r'^search/$', login_required(core.views.SearchView.as_view()), name='search'),
    url(r'^stat/$', login_required(core.views.stat_yearly), name='stat'),
    url(r'^stat/yearly/$', login_required(core.views.stat_yearly), name='stat_yearly'),
    url(r'^stat/monthly/$', login_required(core.views.stat_monthly), name='stat_monthly'),
    url(r'^stat/weekdays/$', login_required(core.views.stat_weekdays), name='stat_weekdays'),
    url(r'^top/$', login_required(core.views.top_posters), name='top'),
    url(r'^top/posters/$', login_required(core.views.top_posters), name='top_posters'),
    url(r'^top/shared/posts/$', login_required(core.views.top_shared_posts), name='top_shared_posts'),
    url(r'^top/commented/posts/$', login_required(core.views.top_commented_posts), name='top_commented_posts'),
    url(r'^top/liked/posts/$', login_required(core.views.top_liked_posts), name='top_liked_posts'),
    url(r'^author/(?P<hashid>.+)/$', login_required(core.views.author_posts), name='author_posts'),
    url(r'^facts/$', login_required(core.views.group_activity), name='facts'),
    url(r'^facts/activity/$', login_required(core.views.group_activity), name='group_activity'),
    url(r'^facts/growth/$', login_required(core.views.group_growth), name='group_growth'),
]

handler404 = 'core.views.not_found'
handler500 = 'core.views.server_error'
