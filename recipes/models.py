from django.db import models


class User(models.Model):
    pass


class Recipe(models.Model):
    title = models.TextField(default='')
    ingredients = models.TextField(default='')
    directions = models.TextField(default='')
    servings = models.TextField(default='')
    user = models.ForeignKey(User, default=None)
    url = models.TextField(default='')
    url_name = models.TextField(default='')




