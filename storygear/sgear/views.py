from django.shortcuts import render_to_response
from storygear.core import RestMixin


class StoryHomeView(RestMixin):

    def get(self, *args, **kwargs):
        return render_to_response("index.html")