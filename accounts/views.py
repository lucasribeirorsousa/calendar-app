from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from accounts.forms import SignInForm


class SignInView(View):
    """ User registration view """

    template_name = "accounts/signin.html"
    login_form = SignInForm

    def get(self, request, *args, **kwargs):
        forms = self.login_form()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.login_form(request.POST)
        if forms.is_valid():
            email = forms.cleaned_data["email"]
            password = forms.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("calendar_app:calendar_home")
        context = {"form": forms}
        return render(request, self.template_name, context)
