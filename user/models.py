from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('У пользователя должен быть email')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("эл. почта", unique=True, max_length=100)
    name = models.CharField("имя", max_length=30)
    is_active = models.BooleanField("активированный аккаунт", default=True)
    is_staff = models.BooleanField(default=False)
    activation_code = models.UUIDField("код активации", unique=True, default=uuid.uuid4)
    purchased_books = models.ManyToManyField('book.Book', blank=True, related_name='buyers')
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
