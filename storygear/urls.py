from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^story/', include("sgear.urls")),
    url(r'^$', RedirectView.as_view(pattern_name='story', permanent=True)),
]
