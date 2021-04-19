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


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            username=self.model.normalize_username(username)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password):
        return self._create_user(username, email, password)

    def create_superuser(self, username, email, password):
        user = self._create_user(username, email, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    objects = UserManager()


# class User(User):
#     email = models.EmailField(verbose_name='email', max_length=60, unique=True)
#
#     created_at = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']
#
#     objects = UserManager()
#
#     def __str__(self):
#         return self.username
#
#     def has_perm(self, permission, obj=None):
#         return self.is_admin
#
#     def has_module_perms(self, app_label):
#         return True


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






