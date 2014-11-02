from django.shortcuts import redirect, render

from recipes.models import Recipe, User


def home(request):
    return render(request, 'home.html')


def add_user(request):
    user_ = User.objects.create()
    return redirect('/users/%d/' % user_.id, {'user': user_})


def add_recipe(request, user_id):
    if request.method == 'POST':
        user_ = User.objects.get(id=user_id)
        recipe = Recipe()
        recipe.title = request.POST.get('recipe_title', '')
        recipe.ingredients = request.POST.get('recipe_ingredients', '')
        recipe.directions = request.POST.get('recipe_directions', '')
        recipe.servings = request.POST.get('recipe_servings', '')
        recipe.user = user_
        recipe.save()
        return redirect('/users/%d/' % int(user_id))

    return render(request, 'add.html')


def user(request, user_id):
    user_ = User.objects.get(id=user_id)
    return render(request, 'user.html', {'user': user_})