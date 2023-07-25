from main.models import Note
from django.forms import ModelForm, TextInput, Textarea
from django.forms import CharField, PasswordInput, ValidationError
from django.contrib.auth.models import User


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'text', 'last_save', 
                  'owner', 'editor', 'viewer']
        widgets = {
            "title": TextInput(attrs={
                "placeholder" : "Title"
            }),
            "text": Textarea(attrs={
                "placeholder" : "Note"
            })
        }


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