from main.models import Note
from django.forms import ModelForm, TextInput, Textarea

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'text', 'last_save']
        widgets = {
            "title": TextInput(attrs={
                "placeholder" : "Title"
            }),
            "text": TextInput(attrs={
                "placeholder" : "Note"
            })
        }