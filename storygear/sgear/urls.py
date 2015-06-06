from django.conf.urls import include, url
from storygear.sgear.views import StoryHomeView, SingleStoryView, NewStoryView

urlpatterns = [
    url(r'^$', StoryHomeView(), name="story"),
    url(r'^(\d+)/$', SingleStoryView(), name="single_story"),
    url(r'^(\d+)/$', NewStoryView(), name="new_story"),
]
