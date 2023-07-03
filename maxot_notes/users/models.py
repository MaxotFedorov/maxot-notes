from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
   if created:
      Profile.objects.create(user=instance)


class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   image = models.ImageField(default='default_profile_pics.jpg',
                                     upload_to='profile_pics/')
   def __str__(self):
      return f'{self.user.username} profile'
