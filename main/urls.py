from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from django.views.generic.base import TemplateView

import main.web as web

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ndex.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', login_required(web.Home.as_view())),

    url(r'^add-collection/', login_required(web.AddCollection.as_view())),
    url(r'^delete-collection/', login_required(web.DeleteCollection.as_view())),
    url(r'^(?P<collection_id>\d+)/', login_required(web.CollectionView.as_view())),

    url(r'^add-cardset/', login_required(web.AddCardSet.as_view())),
    url(r'^delete-cardset/', login_required(web.DeleteCardSet.as_view())),
    url(r'^(?P<collection_id>\d+)/(?P<cardset_id>\d+)/', login_required(web.CardView.as_view())),
)
