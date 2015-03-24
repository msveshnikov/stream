from django.conf.urls import patterns, include, url
from django.contrib import admin

from stream.views import *

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'first.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       # ex: /polls/
                       url(r'^$', index, name='index'),
                       # ex: /polls/5/
                       url(r'^(?P<question_id>\d+)/$', detail, name='detail'),
                       # ex: /polls/5/results/
                       url(r'^(?P<question_id>\d+)/results/$', results, name='results'),
                       # ex: /polls/5/vote/
                       url(r'^(?P<question_id>\d+)/vote/$', vote, name='vote'),
                       ('^hello/$', hello),
                       ('^time/$', current_datetime),
                       (r'^time/plus/(\d{1,2})/$', hours_ahead),
                       url(r'^admin/', include(admin.site.urls)))
