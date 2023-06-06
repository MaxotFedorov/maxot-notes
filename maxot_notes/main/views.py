from django.shortcuts import render, redirect
from django.db.models import Q
from main.models import Note
from main.forms import NoteForm
from django.views.generic import DetailView, UpdateView, ListView
from datetime import datetime
import re


def main(request):
    notes = Note.objects.order_by('-last_save')
    return render(request, 'main/main.html', {'notes' : notes})


def create(request):
    error = ''
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
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
        query = self.request.GET.get('search')
        notes = Note.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )
        return notes