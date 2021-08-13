from django.shortcuts import render
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = "index.html"


class LoginView(generic.TemplateView):
    template_name = "login.html"


class SignupView(generic.TemplateView):
    template_name = "signup.html"


# Create your views here.
