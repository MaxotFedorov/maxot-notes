from django.shortcuts import render, redirect
from main.models import Note
from main.forms import NoteForm
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