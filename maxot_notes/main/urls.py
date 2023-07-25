from django.urls import path
from . import views

urlpatterns = [
    path('', views.NoteListView.as_view(), name='main'),
    path('create/', views.NoteFormView.as_view(), name='create'),
    path('note_<int:pk>/', views.NoteDetailView.as_view(), name='note'),
    path('note_<int:pk>/edit/', views.NoteUpdateView.as_view(), name='note_edit'),
    path('note_<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
    path('search/', views.SearchListView.as_view(), name='search'),
]