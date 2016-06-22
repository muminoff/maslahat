from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import core.views

# Examples:
# url(r'^$', 'maslahat.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', core.views.index, name='index'),
    url(r'^stat/yearly/$', core.views.stat_yearly, name='stat_yearly'),
    url(r'^stat/monthly/$', core.views.stat_monthly, name='stat_monthly'),
    url(r'^stat/weekdays/$', core.views.stat_weekdays, name='stat_weekdays'),
    url(r'^top/posters/$', core.views.top_posters, name='top_posters'),
    url(r'^top/shared/posts/$', core.views.top_shared_posts, name='top_shared_posts'),
    # url(r'^admin/', include(admin.site.urls)),
]
