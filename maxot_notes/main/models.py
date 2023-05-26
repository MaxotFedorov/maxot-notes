from django.db import models

class Note(models.Model):
    title = models.CharField('title', max_length=64, blank=True)
    text = models.TextField('text')
    last_save = models.DateTimeField('last_save', blank=True)

    def __str__(self):
        return self.title