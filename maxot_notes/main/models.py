from typing import Set
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver

class Note(models.Model):
    title = models.CharField('title', max_length=64, blank=True)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_note')
    viewers = models.ManyToManyField(User, blank=True, related_name='viewable_note')
    editors = models.ManyToManyField(User, blank=True, related_name='editable_note')  
    is_public = models.BooleanField(default=True)
    parent_note = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='related_sub_notes')
    sub_notes = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='related_parent_note')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self) -> Set[str]:
        return f'/note_{self.id}'
    
@receiver(post_save, sender=Note)
def update_sub_notes(sender, instance, **kwargs):
    if instance.parent_note:
        instance.parent_note.sub_notes.add(instance)