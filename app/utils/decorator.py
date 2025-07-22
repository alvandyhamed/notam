from functools import wraps

from app.services.notam_services import NotamContext
from app.services.strategies.notam_strategy import NotamStrategy


def notam_decorato(cls):
    """Decorator to inject context into all HTTP methods of a Resource class."""
    methods = ['get', 'post', 'put', 'delete']

    for method_name in methods:
        if hasattr(cls, method_name):
            original_method = getattr(cls, method_name)

            @wraps(original_method)
            def new_method(self, *args, original_method=original_method, **kwargs):
                context = NotamContext(NotamStrategy())  # مقداردهی context
                return original_method(self, context, *args, **kwargs)

            setattr(cls, method_name, new_method)

    return cls