from django.shortcuts import redirect, render, get_object_or_404

from recipes.models import Recipe, User


def home(request):
    return render(request, 'home.html')

    
def about(request):
    return render(request, 'about.html')

    
def contact(request):
    return render(request, 'contact.html')

    
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
        recipe.url_name = recipe.title.lower().replace(' ', '-')
        recipe.url = '/users/%s/recipe/%s' % (user_id, recipe.url_name)
        recipe.save()
        return redirect('/users/%d/' % int(user_id))

    return render(request, 'add.html')


def user(request, user_id):
    user_ = User.objects.get(id=user_id)
    return render(request, 'user.html', {'user': user_})


def view_recipe(request, user_id, recipe_url_name):
    user_ = User.objects.get(id=user_id)
    recipe_ = get_object_or_404(Recipe, url_name=recipe_url_name, user=user_)
    ingredients = recipe_.ingredients.split('\n')
    directions = recipe_.directions.split('\n')
    return render(request, 'recipe.html', {'recipe': recipe_,
                                           'ingredients': ingredients,
                                           'directions': directions})

def save_recipe(request, user_id, recipe_url_name):
    user_ = User.objects.get(id=user_id)
    recipe = get_object_or_404(Recipe, url_name=recipe_url_name, user=user_)
    recipe.title = request.POST.get('recipe_title', '')
    recipe.ingredients = request.POST.get('recipe_ingredients', '')
    recipe.directions = request.POST.get('recipe_directions', '')
    recipe.servings = request.POST.get('recipe_servings', '')
    recipe.user = user_
    recipe.url_name = recipe.title.lower().replace(' ', '-')
    recipe.url = '/users/%s/recipe/%s' % (user_id, recipe.url_name)
    recipe.save()
    return redirect('/users/%d/' % int(user_id))

