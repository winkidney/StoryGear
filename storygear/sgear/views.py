from django.shortcuts import redirect, get_object_or_404
from django.template import RequestContext
from storygear import RestMixin
from storygear.sgear.forms import NewStoryForm, EditStoryForm, NewChapterForm
from storygear.sgear.models import Story, Chapter


class StoryHomeView(RestMixin):

    def get(self, request, *args, **kwargs):
        """
        :type request: django.http.request.HttpRequest
        """
        stories = Story.objects.order_by("ctime")[0:2]
        # todo: change slice
        return self.render("index.html", locals())


class SingleStoryView(RestMixin):

    def get(self, request, story_id, *args, **kwargs):
        story = Story.objects.get(id=story_id)
        return self.render("one_story/read.html", locals())


class NewStoryView(RestMixin):

    def get(self, request, *args, **kwargs):
        form = NewStoryForm()
        return self.render("one_story/new.html", locals())

    def post(self, request, *args, **kwargs):
        form = NewStoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect(story)
        return self.render("one_story/new.html", locals())


class EditStoryView(RestMixin):

    def get(self, request, story_id, *args, **kwargs):
        story = get_object_or_404(Story, pk=story_id)
        form = EditStoryForm(instance=story)
        return self.render("one_story/edit.html", locals())

    def post(self, request, story_id, *args, **kwargs):
        story = get_object_or_404(Story, pk=story_id)
        form = EditStoryForm(data=request.POST, instance=story)
        if form.is_valid():
            form.save()
            return redirect(story)
        return self.render("one_story/edit.html", locals())

class NewChapterView(RestMixin):

    def get(self, request, story_id, *args, **kwargs):
        story = get_object_or_404(Story, pk=story_id)
        form = NewChapterForm()
        return self.render("one_story/new_chapter.html", locals())

    def post(self, request, story_id, *args, **kwargs):
        story = get_object_or_404(Story, pk=story_id)
        form = NewChapterForm()
        if form.is_valid():
            rchapter = form.save(commit=False)
            rchapter.author = request.user
            rchapter.save()
            chapter = story.add_chapter(rchapter)
            return redirect(chapter)
        return self.render("one_story/new_chapter.html", locals())

class ChapterAction(RestMixin):

    def post(self, request, story_id, chapter_id, *args, **kwargs):
        raise NotImplementedError("Operation not implemented.")

