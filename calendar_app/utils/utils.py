from django.shortcuts import redirect
from django.urls import reverse

def custom_authentication_required(view):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('accounts:signin'))
        return view(request, *args, **kwargs)
    return _wrapped_view