# coding: utf-8

from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import redirect, get_object_or_404
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
            story.new_chapter()
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

class SingleChapterView(RestMixin):
    def get(self, request, story_id, chapter_index, **kwargs):
        story = get_object_or_404(Story, pk=story_id)
        chapter = Chapter.get_by_story(story_id, chapter_index)
        if chapter is None:
            raise Http404
        return self.render("one_story/chapter/read.html", locals(), use_context=False)


class NewChapterView(RestMixin):

    def get(self, request, story_id, *args, **kwargs):
        story = get_object_or_404(Story, pk=story_id)
        form = NewChapterForm()
        return self.render("one_story/new_chapter.html", locals())

    def post(self, request, story_id, *args, **kwargs):
        story = get_object_or_404(Story, pk=story_id)
        form = NewChapterForm(request.POST)
        if form.is_valid():
            rchapter = form.save(commit=False)
            rchapter.author = request.user
            rchapter.save()
            chapter = story.add_rchapter(rchapter)
            return redirect("/story/%s/%s" % (story_id, chapter.relative_url))
        return self.render("one_story/new_chapter.html", locals())

class ChapterActionView(RestMixin):

    def get(self, request, story_id, chapter_index, action, **kwargs):
        self.story_id = story_id
        self.chapter_index = chapter_index

        if hasattr(self, ('action_' + action)):
            return getattr(self, ("action_" + action))()
        else:
            return HttpResponseBadRequest(u"功能不存在或者建设中")

    def action_end(self):
        story = get_object_or_404(Story, pk=self.story_id)
        story.end_start_chapter()
        return HttpResponse(u"章节锁定成功，新章节已创建")


class UnderConstructionView(RestMixin):

    def get(self, request, *args, **kwargs):
        return HttpResponse(u"功能建设中".encode("utf-8"))