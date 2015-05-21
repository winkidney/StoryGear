from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, auto_created=True)


class Tag(models.Model):

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name_plural = u"Chapter"
        verbose_name = u"Chapter"
        ordering = ['ctime']
        db_table = "tags"

    name = models.CharField(max_length=250, db_index=True, verbose_name="title")
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

    title = models.CharField(max_length=255, verbose_name=u'name', db_index=True)
    description = models.TextField(verbose_name=u'description')
    content = models.TextField()

    rank = models.IntegerField(default=0, db_index=True)
    is_draft = models.BooleanField(default=False, db_index=True)

    author = models.ForeignKey(User, null=True, blank=False)
    ctime = models.ForeignKey(default=0)


class Chapter(models.Model):
    def __unicode__(self):
        return u"%s" % self.title

    class Meta:
        verbose_name_plural = u"Chapter"
        verbose_name = u"Chapter"
        ordering = ['title']
        db_table = "chapters"

    rchapters = models.ManyToManyField(RChapter)
    index = models.IntegerField(default=0, null=False, blank=False, db_index=True)
    selected = models.ForeignKey(RChapter)


class Story(models.Model):

    def __unicode__(self):
        return u"%s" % self.title

    class Meta:
        verbose_name_plural = u"Stories"
        verbose_name = u"Story"
        ordering = ['ctime']

    title = models.CharField(max_length=255, verbose_name=u'name', db_index=True)
    description = models.TextField(verbose_name=u'description')

    tags = models.ManyToManyField("Tag")

    chapter_count = models.IntegerField(default=0, verbose_name=u"Count")
    chapters = models.ManyToManyField(Chapter, verbose_name=u"Count")

    author = models.ForeignKey(User)
    is_draft = models.BooleanField(default=False, db_index=True)

    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)



