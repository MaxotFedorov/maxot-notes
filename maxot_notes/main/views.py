from django.shortcuts import redirect
from django.db.models import Q
from main.models import Note
#from django.contrib.auth.decorators import login_required
from main.forms import NoteForm
from django.http import HttpResponseForbidden
from django.views.generic import DetailView, UpdateView, \
                                ListView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datetime import datetime
import re


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'main/main.html'
    context_object_name = 'notes'

    def get_queryset(self):
        notes = Note.objects.filter(
            Q(owner=self.request.user) | 
            Q(editor=self.request.user) |
            Q(viewer=self.request.user)
        ).order_by('-last_save')
        return notes
    
    
class SearchListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'main/main.html'
    context_object_name = 'notes'

    def get_queryset(self):
        query = self.request.GET.get('search')
        notes = Note.objects.filter(
            (Q(owner=self.request.user) | 
            Q(editor=self.request.user) |
            Q(viewer=self.request.user))                
            & (Q(title__icontains=query) | 
                Q(text__icontains=query))
        ).order_by('-last_save')
        return notes


class NoteFormView(LoginRequiredMixin, FormView):
    template_name = "main/create.html"
    form_class = NoteForm
    success_url = "/"
    
    def form_valid(self, form):
        note = form.save(commit=False)        
        if note.title == '':
            pattern = re.compile(r'\s')
            matches = pattern.finditer(note.text)
            positions = [match.start() for match in matches]
            count = 0
            for position in positions:
                if position < 64:
                    count += 1
            text = note.text.split(' ')[:count]
            text = ' '.join(text)
            note.title = text

        note.last_save = datetime.now()
        if not note.pk:
            note.owner = self.request.user
        note.save()
        editors = form.cleaned_data['editor']
        viewers = form.cleaned_data['viewer']
        note.editor.set(editors)
        note.viewer.set(viewers)
        return redirect('main')


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'main/note.html'
    context_object_name = 'note'

    def dispatch(self, request, *args, **kwargs):
        note = self.get_object()
        if note.viewer.filter(id=request.user.id).exists() or \
            note.editor.filter(id=request.user.id).exists() or \
            note.owner_id == request.user.id:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to access this note.") 
        
        
class NoteDeleteView(DeleteView):
    model = Note


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = 'main/create.html'
    form_class = NoteForm

    def dispatch(self, request, *args, **kwargs):
        note = self.get_object()
        if note.editor.filter(id=request.user.id).exists() or \
            note.owner_id == request.user.id:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to access this note.")       

    def form_valid(self, form):
        note = form.save(commit=False)        
        if note.title == '':
            pattern = re.compile(r'\s')
            matches = pattern.finditer(note.text)
            positions = [match.start() for match in matches]
            count = 0
            for position in positions:
                if position < 64:
                    count += 1
            text = note.text.split(' ')[:count]
            text = ' '.join(text)
            note.title = text

        note.last_save = datetime.now()            
        note.save()
        editors = form.cleaned_data['editor']
        viewers = form.cleaned_data['viewer']
        note.editor.set(editors)
        note.viewer.set(viewers)
        return redirect('main')