from functools import wraps
from flask import abort, request

# def check_is_htmx(request):
#     if not request.headers.get("HX-Request"):
#         abort(403)

# decorator cek apakah request berasal dari htmx
def hx_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.headers.get("HX-Request") != "true":
            abort(403)
        return func(*args, **kwargs)

    return wrapper