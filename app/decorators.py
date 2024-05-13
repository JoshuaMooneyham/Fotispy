from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(req, *args, **kwargs):

            group = None
            if req.user.groups.exists():
                group = req.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(req, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
            
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(req, *a, **kw):
        group = None
        if req.user.groups.exists():
            group = req.user.groups.all()[0].name

        if group == 'Standard':
            return redirect('home')
        elif group == 'Admin':
            return view_func(req, *a, **kw)
        
    return wrapper_function

