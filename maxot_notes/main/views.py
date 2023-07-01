from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from main.models import Note
from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required
from main.forms import NoteForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, UpdateView, ListView, CreateView
from datetime import datetime
import re


def main(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(access=request.user).order_by('-last_save')
        return render(request, 'main/main.html', {'notes' : notes})
    else: return redirect('login')

def create(request):
    error = ''
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            if note.title == '':
                if len(str(note.text)) <= 64:
                    note.title = note.text
                else:
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
            note.access.add(request.user)
            return redirect('main')
        else: 
            error = form.errors

    form = NoteForm()

    return render(request, 'main/create.html', 
                  {'form': form, 'error': error})


class NoteDetailView(DetailView):
    model = Note
    template_name = 'main/note.html'
    context_object_name = 'note'


class NoteUpdateView(UpdateView):
    model = Note
    template_name = 'main/create.html'
    form_class = NoteForm

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

        if note.last_save is None:  
            note.last_save = datetime.now()
            
        note.save()
        return redirect('main')
    

class SearchListView(ListView):
    model = Note
    template_name = 'main/main.html'
    context_object_name = 'notes'


    def get_queryset(self):
        if self.request.user.is_authenticated:
            query = self.request.GET.get('search')
            notes = Note.objects.filter(
                Q(access=self.request.user) & (Q(title__icontains=query) | Q(text__icontains=query))
            ).order_by('-last_save')
            return notes
        else: return redirect('login')


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"