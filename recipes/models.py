from django.db import models


class Recipe(models.Model):
    title = models.TextField(default='')
    ingredients = models.TextField(default='')
    directions = models.TextField(default='')
    servings = models.TextField(default='')
