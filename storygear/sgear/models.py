# coding: utf-8
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, auto_created=True)


class Tag(models.Model):

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name_plural = u"Tags"
        verbose_name = u"Tag"
        ordering = ['name']
        db_table = "tags"

    name = models.CharField(max_length=250, db_index=True, verbose_name="name")
    description = models.TextField()
    story_count = models.BigIntegerField(default=0)


class RChapter(models.Model):
    def __unicode__(self):
        return u"%s" % self.title

    class Meta:
        verbose_name_plural = u"RChapters"
        verbose_name = u"RChapter"
        ordering = ['rank']
        db_table = "rchapters"

    title = models.CharField(max_length=255, verbose_name=u'章节标题', db_index=True)
    description = models.TextField(verbose_name=u'章节简介', blank=False, help_text=u"介绍下你的概要或者想法吧？")
    content = models.TextField(blank=False, verbose_name=u"正文", help_text=u"上方撰写你的内容~")

    rank = models.IntegerField(default=0, db_index=True)
    stars = models.IntegerField(default=0, db_index=True)
    is_draft = models.BooleanField(verbose_name=u"存为草稿", default=False, db_index=True)

    author = models.ForeignKey(User, null=True, blank=False)
    ctime = models.DateTimeField(auto_now_add=True)


class Chapter(models.Model):
    def __unicode__(self):
        return u"%s" % self.index

    class Meta:
        verbose_name_plural = u"Chapter"
        verbose_name = u"Chapter"
        ordering = ['index']
        db_table = "chapters"

    rchapters = models.ManyToManyField(RChapter, blank=True, related_name="rchapters")
    index = models.IntegerField(default=1, null=False, blank=False, db_index=True)
    selected = models.ForeignKey(RChapter, blank=True, null=True, related_name="selected")
    voted = models.BooleanField(default=False, blank=False, null=False, help_text=u"If the best has been voted.")

    def get_child_property(self, name):
        if self.selected:
            return getattr(self.selected, name)

    @property
    def title(self):
        return self.get_child_property("title")

    @property
    def rank(self):
        return self.get_child_property("rank")

    @property
    def stars(self):
        return self.get_child_property("stars")

    def select_chapter(self, chapter):
        self.selected = chapter
        self.voted = True


class Story(models.Model):

    def __unicode__(self):
        return u"%s" % self.title

    class Meta:
        verbose_name_plural = u"Stories"
        verbose_name = u"Story"
        ordering = ['ctime']

    title = models.CharField(max_length=255, verbose_name=u'标题', db_index=True)
    description = models.TextField(verbose_name=u'概要')
    content = models.TextField(blank=True, verbose_name=u"引子")

    tags = models.ManyToManyField(Tag, related_name="tags")

    chapter_count = models.IntegerField(default=0, verbose_name=u"Chapter count")
    chapters = models.ManyToManyField(Chapter, related_name="chapters", verbose_name=u"Chapters")
    latest_chapter = models.IntegerField(default=1, null=False, blank=False)

    rank = models.IntegerField(default=0, null=False, blank=False)
    stars = models.IntegerField(default=0, null=False, blank=False)

    author = models.ForeignKey(User)
    is_draft = models.BooleanField(default=False, db_index=True, verbose_name=u"存为草稿")

    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    def get_chapters(self):
        return self.chapters.order_by("index")

    def get_voted_chapters(self):
        return [chapter for chapter in self.chapters.order_by("index") if chapter.selected]

    def get_absolute_url(self):
        return "/story/%s/" % self.id

    def add_chapter(self, real_chapter):
        try:
            chapter = Chapter.objects.get(id=self.latest_chapter)
        except ObjectDoesNotExist:
            chapter = Chapter(index=self.latest_chapter)
            chapter.save()

        chapter.rchapters.add(real_chapter)
        chapter.save()
        return chapter
