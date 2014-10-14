from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def add(request):
    if request.method == 'POST':
        # TODO -- is there a redirect?
        return render(request, 'home.html',
            {'recipe_title': request.POST['recipe_title']})
    return render(request, 'add.html')