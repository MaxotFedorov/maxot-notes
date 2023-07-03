from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, DetailView
from django.contrib.auth.models import User
from users.forms import ProfileUpdateForm


def user(request, username):
    form = None
    user = User.objects.get(username=username)
    if user.username == request.user.username:
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST, 
                                     request.FILES, 
                                     instance=user.profile)
            if form.is_valid():
                form.save()
        form = ProfileUpdateForm()
    context = {'received_user' : user, 
               'form' : form}
    return render(request, 'users/user.html', context)


def all_users(request):
    user = User.objects.all()
    return render(request, 'users/all_users.html', {'received_users' : user})


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"