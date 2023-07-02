from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, DetailView
from django.contrib.auth.models import User



def user(request, username):
    user = User.objects.get(username=username)
    return render(request, 'users/user.html', {'received_user' : user})


def all_users(request):
    user = User.objects.all()
    return render(request, 'users/all_users.html', {'received_users' : user})

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"