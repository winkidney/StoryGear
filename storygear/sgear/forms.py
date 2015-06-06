from django import forms

class NewStoryForm(forms.Form):

    title = forms.CharField(max_length=250, required=True)
