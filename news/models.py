from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class ConfEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)


class Category(models.Model):
    name = models.TextField()
    created_at = models.DateTimeField(default = datetime.now())


class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default = datetime.now())

    def __str__(self):
        return self.title
    class Meta:
        permissions = [
            ('user', "User can viev news"),
            ('admin', "can do avrething"),
        ]


