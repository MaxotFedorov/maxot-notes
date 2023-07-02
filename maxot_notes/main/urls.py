from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('create', views.create, name='create'),
    path('note_<int:pk>', views.NoteDetailView.as_view(), name='note'),
    path('note_<int:pk>/edit', views.NoteUpdateView.as_view(), name='note_edit'),
    path('search', views.SearchListView.as_view(), name='search'),
]