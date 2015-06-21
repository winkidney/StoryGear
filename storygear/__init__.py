# coding: utf-8

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, Http404, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext


class RestMixin(object):
    _methods = {
        "GET": "get",
        "POST": "post",
        "PUT": "put",
        "DELETE": "delete",
    }

    def __init__(self, decorators=None, query_or_none=True):
        decorators_seq = []

        if isinstance(decorators, (list, tuple)):
            for decorator in decorators:
                if not callable(decorator):
                    raise TypeError("Decorators must be callable: except callable, got %s" % decorator)
                decorators_seq.append(decorator)
        elif callable(decorators):
            decorators_seq.append(decorators)

        self.decorators = tuple(decorators_seq)

        self.query_or_none = query_or_none

    def call(self, function, *args, **kwargs):
        for decorator in self.decorators:
                function = decorator(function)
        try:
            return function(self.request, *args, **kwargs)
        except (ObjectDoesNotExist, Http404):
            if self.query_or_none:
                return HttpResponseNotFound(u"你访问的对象不存在：），有问题请联系winkidney@gmail.com")
            else:
                raise

    def __call__(self, request, *args, **kwargs):
        """
        :param request: django http request object
        :type request: django.http.request.HttpRequest
        :return: HttpResponse
        """
        self.request = request
        view_func_name = self._methods.get(request.method, None)
        if view_func_name is not None:
            return self.call(getattr(self, view_func_name), *args, **kwargs)
        else:
            return self.raise_400(view_func_name)

    @staticmethod
    def raise_400():
            return HttpResponseBadRequest("Given http method not implement.")

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

