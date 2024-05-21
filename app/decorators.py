from django.http import HttpResponse # type: ignore
from django.shortcuts import redirect # type: ignore

def unauthenticated_user(view_func): # type: ignore
    def wrapper_func(request, *args, **kwargs): # type: ignore
        if request.user.is_authenticated: # type: ignore
            return redirect('home')
        else:
            return view_func(request) # type: ignore

    return wrapper_func # type: ignore

def allowed_users(allowed_roles=[]): # type: ignore
    def decorator(view_func): # type: ignore
        def wrapper_func(req, *args, **kwargs): # type: ignore

            group = None
            if req.user.groups.exists(): # type: ignore
                group = req.user.groups.all()[0].name # type: ignore
            
            if group in allowed_roles:
                return view_func(req, *args, **kwargs) # type: ignore
            else:
                return HttpResponse('You are not authorized to view this page')
            
        return wrapper_func # type: ignore
    return decorator # type: ignore

def admin_only(view_func): # type: ignore
    def wrapper_function(req, *a, **kw): # type: ignore
        group = None
        if req.user.groups.exists(): # type: ignore
            group = req.user.groups.all()[0].name # type: ignore

        if group == 'Standard':
            return redirect('home')
        elif group == 'Admin':
            return view_func(req, *a, **kw) # type: ignore
        
    return wrapper_function # type: ignore

