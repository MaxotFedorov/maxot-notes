from main.models import Note
from django.forms import ModelForm, TextInput, Textarea
from django.forms import CharField, PasswordInput, ValidationError
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'viewers', 'editors', 'is_public', 'parent_note']
        widgets = {
            "title": TextInput(attrs={
                "placeholder" : "Title"
            }),
            'content': CKEditorWidget(),
        }
        
        
class NoteUpdateForm(NoteForm):
    class Meta(NoteForm.Meta):
        exclude = ['owner']


class UserRegistrationForm(ModelForm):
    password = CharField(label='Password', widget=PasswordInput)
    password2 = CharField(label='Repeat password', widget=PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def password_match(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Passwords don\'t match.')
        return cd['password2']