from django import forms
from storygear.sgear.models import Story, RChapter


class NewStoryForm(forms.ModelForm):

    class Meta:
        model = Story
        fields = ("title", "description", "content", "is_draft")


class EditStoryForm(forms.ModelForm):

    class Meta:
        model = Story
        fields = ("title", "description", "content", "is_draft")


class NewChapterForm(forms.ModelForm):

    class Meta:
        model = RChapter
        fields = ("title", "description", "content", "is_draft")