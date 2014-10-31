from django.shortcuts import redirect, render

from recipes.models import Recipe, User


def home(request):
    return render(request, 'home.html')


def add_user(request):
    user = User.objects.create()
    return redirect('/users/ben/', {'user': user})


def add_recipe(request):
    if request.method == 'POST':
        recipe = Recipe()
        recipe.title = request.POST.get('recipe_title', '')
        recipe.ingredients = request.POST.get('recipe_ingredients', '')
        recipe.directions = request.POST.get('recipe_directions', '')
        recipe.servings = request.POST.get('recipe_servings', '')
        #recipe.user = request.POST.get('user', '')
        recipe.save()
        return redirect('/users/ben/')

    return render(request, 'add.html')


def user(request):
    recipes = Recipe.objects.all()
    return render(request, 'user.html', {'recipes': recipes})