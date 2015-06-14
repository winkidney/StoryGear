from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from storygear.sgear.views import StoryHomeView, SingleStoryView, NewStoryView, EditStoryView, NewChapterView


urlpatterns = (
    url(r'^$', StoryHomeView(), name="story"),
    url(r'^(\d+)/$', SingleStoryView(), name="single_story"),
    url(r'^(\d+)/edit/$', EditStoryView(), name="edit_story"),
    url(r'^(\d+)/new_chapter/$', NewChapterView(), name="new_chapter"),
    url(r'^new/$', NewStoryView(), name="new_story"),
)