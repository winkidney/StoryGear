from django.shortcuts import render_to_response
from storygear import RestMixin
from storygear.sgear.models import Story


class StoryHomeView(RestMixin):

    def get(self, *args, **kwargs):
        stories = Story.objects.order_by("ctime")[0:2]
        return render_to_response("index.html", locals())


class SingleStoryView(RestMixin):

    def get(self, story_id, *args, **kwargs):
        story = Story.objects.get(id=story_id)
        return render_to_response("one_story/read.html", locals())

    def put(self, story_id, *args, **kwargs):
        raise NotImplementedError("This resource can not be modified")