from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.views.generic import (
    DetailView, UpdateView, 
    ListView, FormView, DeleteView
)
from main.forms import NoteForm, NoteUpdateForm
from main.mixins import NoteSaveMixin
from main.models import Note


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'main/main.html'
    context_object_name = 'notes'

    def get_queryset(self):
        notes = Note.objects.filter(
            Q(owner=self.request.user) | 
            Q(editors=self.request.user) |
            Q(viewers=self.request.user) |
            Q(is_public=True) 
        ).order_by('-last_edited_at')
        return notes
    
    
class SearchListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'main/main.html'
    context_object_name = 'notes'

    def get_queryset(self):
        query = self.request.GET.get('search')
        notes = Note.objects.filter(
            (Q(owner=self.request.user) | 
            Q(editors=self.request.user) |
            Q(viewers=self.request.user) |
            Q(is_public=True) )                
            & (Q(title__icontains=query) | 
               Q(content__icontains=query))
        ).order_by('-last_edited_at')
        return notes


class NoteCreateView(LoginRequiredMixin, NoteSaveMixin, FormView):
    model = Note
    template_name = "main/create.html"
    form_class = NoteForm
    success_url = reverse_lazy('main')
    
    def form_valid(self, form):
        parent_note_id = self.kwargs.get('parent_note_id')
        parent_note = None
        if parent_note_id:
            parent_note = Note.objects.get(pk=parent_note_id)
        note = form.save(commit=False)
        if parent_note:
            note.parent_note = parent_note
        self.save_note(form)
        return redirect('main')
    

class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'main/note.html'
    context_object_name = 'note'

    def has_permission(self, note):
        return (
            note.viewers.filter(id=self.request.user.id).exists()
            or note.editors.filter(id=self.request.user.id).exists()
            or note.owner_id == self.request.user.id
            or note.is_public == True
        )

    def dispatch(self, request, *args, **kwargs):
        note = self.get_object()
        if self.has_permission(note):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to access this note.") 
        
        
class NoteDeleteView(DeleteView):
    model = Note
    success_url = '/'
    template_name = 'main/delete.html'
    

class NoteUpdateView(LoginRequiredMixin, NoteSaveMixin, UpdateView):
    model = Note
    template_name = 'main/create.html'
    form_class = NoteUpdateForm

    def has_permission(self, note):
        return (
            note.editors.filter(id=self.request.user.id).exists()
            or note.owner_id == self.request.user.id
    )

    def dispatch(self, request, *args, **kwargs):
        note = self.get_object()
        if self.has_permission(note):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to access this note.")
        
    def form_valid(self, form):
        self.save_note(form)
        return super().form_valid(form)