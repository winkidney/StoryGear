from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import RequestContext


class RestMixin(object):
    _methods = {
        "GET": "get",
        "POST": "post",
        "PUT": "put",
        "DELETE": "delete",
    }

    def __init__(self, decorators=None):
        decorators_seq = []

        if isinstance(decorators, (list, tuple)):
            for decorator in decorators:
                if not callable(decorator):
                    raise TypeError("Decorators must be callable: except callable, got %s" % decorator)
                decorators_seq.append(decorator)
        elif callable(decorators):
            decorators_seq.append(decorators)

        self.decorators = tuple(decorators_seq)

    def call(self, function, *args, **kwargs):
        for decorator in self.decorators:
                function = decorator(function)
        return function(self.request, *args, **kwargs)

    def __call__(self, request, *args, **kwargs):
        """
        :param request: django http request object
        :type request: django.http.request.HttpRequest
        :return: HttpResponse
        """
        self.request = request
        view_func = self._methods.get(request.method, None)
        if view_func is not None:
            return getattr(self, view_func)(request, *args, **kwargs)
        else:
            return self.raise_400()

    @staticmethod
    def raise_400():
            return HttpResponseBadRequest("Method not implement.")

    def get(self, request, *args, **kwargs):
        return self.raise_400()

    def post(self, request, *args, **kwargs):
        return self.raise_400()

    def put(self, request, *args, **kwargs):
        return self.raise_400()

    def delete(self, request, *args, **kwargs):
        return self.raise_400()

    def render(self, template_name, context_dict=None, use_context=True, **kwargs):
        if use_context:
            return render_to_response(template_name, context_dict, context_instance=RequestContext(self.request), **kwargs)
        else:
            return render_to_response(template_name, context_dict, **kwargs)

