# coding: utf-8
from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):

    username = forms.CharField(max_length=250)
    password = forms.PasswordInput()

    def is_valid(self, request):
        """
        :type request: django.http.request.HttpRequest
        :param request:
        :return:
        """
        if not super(LoginForm, self).is_valid():
            return False
        else:
            return authenticate(
                username=self.cleaned_data["username"],
                password=self.cleaned_data["password"],
            )
