from django.http import HttpResponseBadRequest


class RestMixin(object):

    def __init__(self, csrf_exempt=False, decorators=None):
        self.decorators = decorators
        self.csrf_exempt = csrf_exempt

    def call(self, function, *args, **kwargs):
        if self.decorators is None:
            return function(*args, **kwargs)
        elif isinstance(self.decorators, (list, tuple)):
            for decorator in self.decorators:
                function = decorator(function)
            return function(*args, **kwargs)
        else:
            return self.decorators(function)(*args, **kwargs)

    def __call__(self, request, *args, **kwargs):
        """
        :param request: django http request object
        :type request: django.http.request.HttpRequest
        :return: HttpResponse
        """
        self.request = request

        if request.method == "GET":
            return self.call(self.get, *args, **kwargs)
        elif request.method == "POST":
            return self.call(self.post, *args, **kwargs)
        elif request.method == "PUT":
            return self.call(self.put, *args, **kwargs)
        elif request.method == "DELETE":
            return self.call(self.delete, *args, **kwargs)
        else:
            self.raise_400()

    @staticmethod
    def raise_400():
            return HttpResponseBadRequest("Method not implement.")

    def get(self, *args, **kwargs):
        return self.raise_400()

    def post(self, *args, **kwargs):
        return self.raise_400()

    def put(self, *args, **kwargs):
        return self.raise_400()

    def delete(self, *args, **kwargs):
        return self.raise_400()