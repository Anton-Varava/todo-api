from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import AbstractUser, BaseUserManager
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(AbstractUser):
    email = models.EmailField(blank=False)

    def __str__(self):
        return f'User "{self.username}, email - {self.email}"'


class Board(models.Model):
    name = models.CharField(verbose_name='Name', max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Board {}".format(self.name)


class TodoItem(models.Model):
    title = models.CharField(verbose_name='Title', max_length=200)
    isDone = models.BooleanField(verbose_name='Done', default=False)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated at', auto_now=True)
    board = models.ForeignKey(Board, verbose_name='Board', on_delete=models.CASCADE)

    def __str__(self):
        return f"TodoItem {self.title}, status - {('Done' if self.isDone else 'Not done yet')}. " \
               f"Created at {self.created_at}"






