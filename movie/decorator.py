from functools import wraps
from django.http import JsonResponse


def content_type(func):
    @wraps(func)
    def inner_function(self, request, *args, **kwargs):
        if request.headers['content_type'] != 'application/json':
            return JsonResponse({'message': 'Not acceptable'}, status=406)
        return func(self, request, *args, **kwargs)
    return inner_function
