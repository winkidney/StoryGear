from django.conf.urls import include, url
from storygear.sgear.views import StoryHomeView, SingleStoryView

urlpatterns = [
    url(r'^$', StoryHomeView(), name="story"),
    url(r'^(\d+)/$', SingleStoryView(), name="single_story"),
]
