from django.shortcuts import redirect, render, get_object_or_404

from recipes.models import Recipe, User


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
    recipe_ = get_object_or_404(Recipe, url_name=recipe_url_name, user=user_)
    if request.method == 'POST':
        recipe_.title = request.POST.get('recipe_title', '')
        recipe_.ingredients = request.POST.get('recipe_ingredients', '')
        recipe_.directions = request.POST.get('recipe_directions', '')
        recipe_.servings = request.POST.get('recipe_servings', '')
        recipe_.save()
        return redirect('/users/%s/recipe/%s' % (user_.name, recipe_.url_name))
    ingredients = recipe_.ingredients.split('\n')
    directions = recipe_.directions.split('\n')
    return render(request, 'edit.html', {'user_name': user_name,
                                         'recipe': recipe_,
                                         'ingredients': ingredients,
                                         'directions': directions})

