from functools import wraps
from django.shortcuts import redirect


def cliente_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='clientes').exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/acessos/login')
    return _wrapped_view
