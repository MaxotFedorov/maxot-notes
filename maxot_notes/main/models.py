from typing import Set
from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField('title', max_length=64, blank=True)
    text = models.TextField('text')
    last_save = models.DateTimeField('last_save', blank=True)
    owner = models.ForeignKey(User, blank=True,
                              on_delete=models.CASCADE,
                              related_name='oowner_notes')    
    editor = models.ManyToManyField(User, blank=True, 
                                    related_name='editor_notes')
    viewer = models.ManyToManyField(User, blank=True, 
                                    related_name='viewer_notes')
    

    def __str__(self):
        return self.title
    
    def get_absolute_url(self) -> Set[str]:
        return f'/note_{self.id}'