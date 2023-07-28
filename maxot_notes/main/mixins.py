from datetime import datetime
import re

MAX_TITLE_LENGTH = 64

class NoteSaveMixin:    
    def save_note(self, form):
        note = form.save(commit=False) 
        if not note.title:
            pattern = re.compile(r'\s')
            matches = pattern.finditer(note.text)
            positions = [match.start() for match in matches]
            count = 0
            for position in positions:
                if position < MAX_TITLE_LENGTH:
                    count += 1
            if count == 0:
                note.title = note.text[:MAX_TITLE_LENGTH]
            else:
                text = note.text.split(' ')[:count]
                text = ' '.join(text)
                note.title = text

        note.last_save = datetime.now()
        if not note.pk:
            note.owner = self.request.user

        note.save()
        note.editor.set(form.cleaned_data['editor'])
        note.viewer.set(form.cleaned_data['viewer'])
        return note