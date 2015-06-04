from django.contrib import admin

# Register your models here.
from storygear.sgear.models import Chapter, RChapter, Profile, Tag, Story

admin.site.register(Chapter)
admin.site.register(RChapter)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Story)