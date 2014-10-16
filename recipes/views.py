from django.shortcuts import redirect, render

from recipes.models import Recipe


def home(request):
    recipes = Recipe.objects.all()
    return render(request, 'home.html', {'recipes': recipes})


def add(request):
    if request.method == 'POST':
        recipe = Recipe()
        recipe.title = request.POST.get('recipe_title', '')
        recipe.ingredients = request.POST.get('recipe_ingredients', '')
        recipe.directions = request.POST.get('recipe_directions', '')
        recipe.servings = request.POST.get('recipe_servings', '')
        recipe.save()
        return redirect('/')

    return render(request, 'add.html')