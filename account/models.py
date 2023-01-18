from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

class Games(models.Model):
    game_name = models.CharField(max_length=100)
    game_file = models.CharField(max_length=100)
    file_location = models.CharField(max_length=100)
    game_year = models.IntegerField()

    def __str__(self):
        return self.game_name

class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to ='avatars/', null=True, blank=True)
    game = models.ManyToManyField(Games)

    def __str__(self):
        return self.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

