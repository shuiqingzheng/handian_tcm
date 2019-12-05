from django.db import models

# Create your models here.
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, username=None, **extra_fields):
        if not email:
            raise ValueError('邮箱必填')

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, username, **extra_fields)

    def create_superuser(self, email, password, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, username, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, unique=True,)
    username = models.CharField(null=True, blank=True, max_length=125)
    is_staff = models.BooleanField(default=False,)
    is_superuser = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True,)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ('-pk',)
