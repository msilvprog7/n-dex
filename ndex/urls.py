from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from main import controls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ndex.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', controls.Index.as_view()), 
    url(r'^login/', controls.Login.as_view()), 
    url(r'^logout/', controls.Logout.as_view()), 
    url(r'^register/', controls.Register.as_view()), 
    url(r'^home/', include('main.urls')), 
    url(r'^admin/', include(admin.site.urls)), 
)
