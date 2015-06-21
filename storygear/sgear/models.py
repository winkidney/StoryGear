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
    views = models.IntegerField(default=0, db_index=True, null=False, blank=False)
    likes = models.IntegerField(default=0, db_index=True, null=False, blank=False)

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

    @property
    def dchapter(self):
        """
        display chapter
        """
        if self.selected:
            return self.selected
        else:
            if self.rchapters.exists():
                return self.rchapters.order_by("likes")[0]
            return None

    def add_chapter(self, rchapter):
        if not isinstance(rchapter, RChapter):
            raise TypeError("chapter requires RChapter instance.Expect %s, got %s" % (RChapter, rchapter))
        self.rchapters.add(rchapter)
        return rchapter

    @property
    def relative_url(self):
        return "chapter%s/" % self.index

    def select_chapter(self, chapter):
        self.selected = chapter
        self.voted = True

    @classmethod
    def get_by_story(cls, story_id, chapter_index):
        chapters = cls.objects.filter(story__id=story_id, index=chapter_index).all()
        if chapters:
            return chapters[0]
        else:
            return None

    @classmethod
    def end_chapter(cls, chapter_index, selected=None):
        """
        Lock and give a selected chapter to
        :return True if success, false if the chapter does not exist.
        :rtype boolean
        """
        try:
            chapter = cls.objects.get(index=chapter_index)
        except ObjectDoesNotExist:
            return False

        chapter._lock()
        if selected is not None:
            chapter.select_chapter(chapter)

        chapter.save()

        return chapter

    def _lock(self):
        self.voted = True

    def lock(self):
        self._lock()
        self.save()

class Story(models.Model):

    def __unicode__(self):
        return u"%s" % self.title

    class Meta:
        verbose_name_plural = u"Stories"
        verbose_name = u"Story"
        ordering = ['ctime']

    title = models.CharField(max_length=255, verbose_name=u'标题', db_index=True)
    description = models.TextField(verbose_name=u'概要', help_text=u"说说你的想法，比如希望故事怎么发展=w=")
    content = models.TextField(blank=False, verbose_name=u"第零章")

    tags = models.ManyToManyField(Tag, related_name="tags")

    chapter_count = models.IntegerField(default=0, verbose_name=u"Chapter count")
    chapters = models.ManyToManyField(Chapter, related_name="story", verbose_name=u"Chapters")
    latest_chapter = models.IntegerField(default=0, null=False, blank=False)

    rank = models.IntegerField(default=0, db_index=True, null=False, blank=False)
    views = models.IntegerField(default=0, db_index=True, null=False, blank=False)
    likes = models.IntegerField(default=0, db_index=True, null=False, blank=False)
    stars = models.IntegerField(default=0, db_index=True, null=False, blank=False)

    author = models.ForeignKey(User)
    is_draft = models.BooleanField(default=False, db_index=True, verbose_name=u"存为草稿")

    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    def get_chapters(self):
        return self.chapters.order_by("index")

    def get_absolute_url(self):
        return "/story/%s/" % self.id

    @property
    def voting_chapter(self):
        return RChapter.objects.get(index=self.latest_chapter)

    def add_rchapter(self, real_chapter):
        """
        :rtype Chapter
        """
        chapter = Chapter.objects.get(index=self.latest_chapter)

        chapter.add_chapter(real_chapter)
        self.chapter_count += 1
        chapter.save()
        self.save()
        return chapter

    def new_chapter(self):
        self.latest_chapter += 1
        new_chapter = Chapter(index=self.latest_chapter)
        new_chapter.save()

        self.chapters.add(new_chapter)
        self.save()

    def end_start_chapter(self, chapter_selected=None):
        chapter = Chapter.objects.get(index=self.latest_chapter)
        chapter.end_chapter(self.latest_chapter, chapter_selected)

        self.new_chapter()