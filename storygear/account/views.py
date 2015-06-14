from storygear import RestMixin


class LoginView(RestMixin):

    def get(self, request, *args, **kwargs):
        form = request
        pass