from datetime import datetime
import re

MAX_TITLE_LENGTH = 64

class NoteSaveMixin:    
    def save_note(self, form):
        note = form.save(commit=False) 
        if not note.title:
            pattern = re.compile(r'\s')
            matches = pattern.finditer(note.content)
            positions = [match.start() for match in matches]
            count = 0
            for position in positions:
                if position < MAX_TITLE_LENGTH:
                    count += 1
            if count == 0:
                note.title = note.content[:MAX_TITLE_LENGTH]
            else:
                content = note.content.split(' ')[:count]
                content = ' '.join(content)
                note.title = content
        
        note.last_edited_at = datetime.now()
        if not note.pk:
            note.owner = self.request.user

        note.save()
        note.editors.set(form.cleaned_data['editors'])
        note.viewers.set(form.cleaned_data['viewers'])
        return note