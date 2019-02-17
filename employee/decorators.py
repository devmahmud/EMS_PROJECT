from django.core.exceptions import PermissionDenied


def role_required(allowed_roles=[]):
    def decorator(func):
        def wrap(request, *args, **kwargs):
            if request.role in allowed_roles:
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return wrap
    return decorator
