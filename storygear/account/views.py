from django.http import HttpResponse
from storygear import RestMixin


class ProfileView(RestMixin):

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.request.user.username)
