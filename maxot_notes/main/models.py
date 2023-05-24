from django.db import models

class Note(models.Model):
    title = models.CharField('title', max_length=64)
    text = models.TextField('text')
    last_save = models.DateTimeField('last_save')

    def __str__(self):
        return self.title