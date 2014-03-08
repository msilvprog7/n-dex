from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from django.views.generic.base import TemplateView

import main.web as web

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ndex.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', login_required(web.Home.as_view())),

)
