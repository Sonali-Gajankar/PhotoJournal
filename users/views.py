from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import RegisterUserForm

# Create your views here.
from django.urls import reverse


def home(request):
    return render(request, "journal/home.html")


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    
    def form_valid(self, form):
        return super(RegisterUser, self).form_valid(form)

    def get_success_url(self):
        return reverse('login')