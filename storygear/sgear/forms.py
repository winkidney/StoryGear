from bootstrap_toolkit.widgets import BootstrapTextInput
from django import forms
from storygear.sgear.models import Story


class NewStoryForm(forms.ModelForm):

    class Meta:
        model = Story
        fields = ("title", "description", "content", "is_draft")