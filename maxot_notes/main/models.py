from typing import Set
from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField('title', max_length=64, blank=True)
    text = models.TextField('text')
    last_save = models.DateTimeField('last_save', blank=True)
    access = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self) -> Set[str]:
        return f'/note_{self.id}'