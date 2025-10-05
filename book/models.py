from django.db import models
from user.models import User

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)

    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    users = models.ManyToManyField(
        to=User,
        related_name='books',
        blank=True
    )

    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title