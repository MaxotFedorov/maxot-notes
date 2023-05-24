from django.shortcuts import render
from main.models import Note

def index(request):
    notes = Note.objects.all()
    return render(request, 'main/main.html', {'notes' : notes})