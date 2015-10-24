from django.db import models


class User(models.Model):
    name = models.TextField(default='')
    display_name = models.TextField(default='')

    def __str__(self):
        return self.display_name


class Recipe(models.Model):
    title = models.TextField(default='', unique=True)
    ingredients = models.TextField(default='')
    directions = models.TextField(default='')
    servings = models.TextField(default='', blank=True)
    user = models.ForeignKey(User, default=None)
    url = models.TextField(default='', blank=True)
    url_name = models.TextField(default='', blank=True)
    source = models.TextField(default='', blank=True)
    source_url = models.TextField(default='', blank=True)
    img_url = models.TextField(default='', blank=True)
    cooking_time = models.TextField(default='', blank=True)
    total_time = models.TextField(default='', blank=True)
    notes = models.TextField(default='', blank=True)

    def __str__(self):
        return self.title
