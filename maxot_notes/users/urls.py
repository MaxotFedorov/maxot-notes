from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_users, name='all_users'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('<slug:username>', views.user, name='username'),
]