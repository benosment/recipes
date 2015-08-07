from django.shortcuts import redirect, render, get_object_or_404
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse

from .models import User, Recipe

import os
import shutil
import logging


def home(request):
    if request.method == 'POST':
        user_ = User()
        user_.display_name = request.POST.get('user_name', '')
        user_.name = user_.display_name.lower()
        user_.save()
        return redirect('/users/%s/' % user_.name, {'user': user_})
    users = User.objects.all()
    return render(request, 'home.html', {'users': users})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def add_recipe(request, user_name):
    if request.method == 'POST':
        user_ = User.objects.get(name=user_name)
        recipe = Recipe()
        recipe.title = request.POST.get('recipe_title', '')
        recipe.ingredients = request.POST.get('recipe_ingredients', '')
        recipe.directions = request.POST.get('recipe_directions', '')
        recipe.servings = request.POST.get('recipe_servings', '')
        recipe.source = request.POST.get('recipe_source', '')
        recipe.source_url = request.POST.get('recipe_source_url', '')
        recipe.cooking_time = request.POST.get('recipe_cooking_time', '')
        recipe.total_time = request.POST.get('recipe_total_time', '')
        recipe.notes = request.POST.get('recipe_notes', '')
        recipe.user = user_
        recipe.url_name = recipe.title.lower().replace(' ', '-')
        recipe.url = '/users/%s/recipe/%s' % (user_name, recipe.url_name)
        recipe.save()
        return redirect('/users/%s/' % user_.name)

    return render(request, 'add.html')


def user(request, user_name):
    user_ = User.objects.get(name=user_name)
    return render(request, 'user.html', {'user': user_})


def view_recipe(request, user_name, recipe_url_name):
    user_ = User.objects.get(name=user_name)
    recipe_ = get_object_or_404(Recipe, url_name=recipe_url_name, user=user_)
    ingredients = recipe_.ingredients.split('\n')
    directions = recipe_.directions.split('\n')
    return render(request, 'recipe.html', {'user_name': user_name,
                                           'recipe': recipe_,
                                           'ingredients': ingredients,
                                           'directions': directions})


def edit_recipe(request, user_name, recipe_url_name):
    user_ = User.objects.get(name=user_name)
    recipe = get_object_or_404(Recipe, url_name=recipe_url_name, user=user_)
    if request.method == 'POST':
        recipe.title = request.POST.get('recipe_title', '')
        recipe.ingredients = request.POST.get('recipe_ingredients', '')
        recipe.directions = request.POST.get('recipe_directions', '')
        recipe.servings = request.POST.get('recipe_servings', '')
        recipe.source = request.POST.get('recipe_source', '')
        recipe.source_url = request.POST.get('recipe_source_url', '')
        recipe.cooking_time = request.POST.get('recipe_cooking_time', '')
        recipe.total_time = request.POST.get('recipe_total_time', '')
        recipe.notes = request.POST.get('recipe_notes', '')
        recipe.save()
        return redirect('/users/%s/recipe/%s' % (user_.name, recipe.url_name))
    ingredients = recipe.ingredients.split('\n')
    directions = recipe.directions.split('\n')
    return render(request, 'edit.html', {'user_name': user_name,
                                         'recipe': recipe,
                                         'ingredients': ingredients,
                                         'directions': directions})


def export(request, username):
    logging.info('received request to export %s' % username)
    zipdir = os.path.join('/tmp', username, 'recipes')
    try:
        os.makedirs(zipdir)
        logging.debug('made directory %s' % zipdir)
        user_ = User.objects.get(name=username)
        for recipe in user_.recipe_set.all():
            filename = os.path.join(zipdir, recipe.url_name)
            with open(filename, 'wt', encoding='utf-8') as f:
                logging.debug('writing %s to %s' % (recipe.title, filename))
                f.write(recipe.title)
                f.write('\n\nIngredients:\n')
                f.write(recipe.ingredients)
                f.write('\n\nDirections:\n')
                f.write(recipe.directions)
                f.write('\n\nServings:\n')
                f.write(recipe.servings)
        shutil.make_archive('recipes', 'zip', os.path.join('/tmp', username), 'recipes')
        shutil.rmtree(zipdir)
        filename = 'recipes.zip'
        wrapper = FileWrapper(open(filename, 'rb'))
        response = HttpResponse(wrapper, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=recipes.zip'
        response['Content-Length'] = os.path.getsize(filename)
        os.remove(filename)
        logging.debug('removing %s' % filename)
    except:
        logging.exception('failed to export')
        shutil.rmtree(zipdir)
        response = None
    return response
