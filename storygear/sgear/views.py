from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from storygear import RestMixin
from storygear.sgear.forms import NewStoryForm
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


class NewStoryView(RestMixin):

    def get(self, *args, **kwargs):
        form = NewStoryForm()
        return render_to_response("one_story/new.html", locals(), context_instance=RequestContext(self.request))

    def post(self, *args, **kwargs):
        form = NewStoryForm(self.request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = self.request.user
            story.save()
            return HttpResponse("Post %s created!" % story.title)
        return render_to_response("one_story/new.html", locals())
