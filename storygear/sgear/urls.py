from django.conf.urls import include, url
from storygear.sgear.views import StoryHomeView

urlpatterns = [
    url(r'^$', StoryHomeView(), name="story"),
]
