from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from recipes.views import home
from recipes.models import Recipe, User


class HomeTest(TestCase):

    def test_root_url_resolves_to_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


class NewRecipeTest(TestCase):

    def test_save_a_post_request_for_an_existing_user(self):
        user = User()
        user.save()
        self.client.post('/users/%d/add_recipe' % user.id,
                         data={'recipe_title': 'new recipe'})
        self.assertEqual(Recipe.objects.count(), 1)
        new_recipe = Recipe.objects.first()
        self.assertEqual(new_recipe.title, 'new recipe')
        self.assertEqual(new_recipe.user, user)

    def test_redirects_after_post(self):
        user = User()
        user.save()
        response = self.client.post('/users/%d/add_recipe' % user.id,
                                    data={'recipe_title': 'Caico e pepe'})
        self.assertRedirects(response, '/users/%d/' % user.id)


class EditRecipeTest(TestCase):

    def test_save_a_post_request_for_an_existing_recipe(self):
        user = User()
        user.save()

        recipe = Recipe()
        recipe.title = 'cacio e pepe'
        recipe.url_name = 'cacio-e-pepe'
        recipe.ingredients = 'kosher salt\n6 oz. pasta \n3 Tbsp. unsalted butter\n 1 tsp. freshly cracked black pepper'
        recipe.directions = 'bring water to a boil\ncook pasta\nadd butter and pepper'
        recipe.servings = '4'
        recipe.user = user
        recipe.save()

        self.client.post('/users/%d/recipe/%s/edit' % (user.id, recipe.url_name),
                         data={'recipe_title': 'Cacio e Pepe'})

        edited_recipe = Recipe.objects.first()
        self.assertEqual(edited_recipe.title, 'Cacio e Pepe')

    def test_redirects_after_save(self):
        user = User()
        user.save()

        recipe = Recipe()
        recipe.title = 'cacio e pepe'
        recipe.url_name = 'cacio-e-pepe'
        recipe.ingredients = 'kosher salt\n6 oz. pasta \n3 Tbsp. unsalted butter\n 1 tsp. freshly cracked black pepper'
        recipe.directions = 'bring water to a boil\ncook pasta\nadd butter and pepper'
        recipe.servings = '4'
        recipe.user = user
        recipe.save()

        response = self.client.post('/users/%d/recipe/%s/edit' % (user.id, recipe.url_name),
                                    data={'recipe_title': 'Cacio e Pepe'})
        self.assertRedirects(response, '/users/%d/recipe/%s' % (user.id, recipe.url_name))

class UserViewTest(TestCase):

    def test_uses_user_template(self):
        user = User.objects.create()
        response = self.client.get('/users/%d/' % user.id)
        self.assertTemplateUsed(response, 'user.html')

    def test_displays_only_recipes_for_that_user(self):
        correct_user = User()
        correct_user.save()
        other_user = User()
        other_user.save()
        Recipe.objects.create(title='cacio e pepe', user=correct_user)
        Recipe.objects.create(title='BA Burger Deluxe', user=correct_user)
        Recipe.objects.create(title='salmon', user=other_user)
        Recipe.objects.create(title='tuna burger', user=other_user)

        response = self.client.get('/users/%d/' % correct_user.id)

        self.assertContains(response, 'cacio e pepe')
        self.assertContains(response, 'BA Burger Deluxe')
        self.assertNotContains(response, 'salmon')
        self.assertNotContains(response, 'tuna burger')

    def test_passes_correct_user_to_template(self):
        user = User.objects.create()
        other_user = User.objects.create()
        response = self.client.get('/users/%d/' % (user.id))
        self.assertEqual(response.context['user'], user)


class RecipeViewTest(TestCase):

    def test_uses_recipe_template(self):
        user = User.objects.create()
        user.save()
        Recipe.objects.create(title='cacio e pepe', url_name='cacio-e-pepe', user=user)
        response = self.client.get('/users/%d/recipe/cacio-e-pepe' % user.id)
        self.assertTemplateUsed(response, 'recipe.html')

    def test_passes_correct_recipe_to_template(self):
        user = User.objects.create()
        user.save()
        recipe = Recipe.objects.create(title='cacio e pepe', url_name='cacio-e-pepe', user=user)
        response = self.client.get('/users/%d/recipe/cacio-e-pepe' % user.id)
        self.assertEqual(response.context['recipe'], recipe)

    def test_displays_valid_recipes_for_that_user(self):
        user = User.objects.create()
        user.save()
        Recipe.objects.create(title='Cacio e Pepe', url_name='cacio-e-pepe', user=user)
        response = self.client.get('/users/%d/recipe/cacio-e-pepe' % user.id)
        self.assertContains(response, 'Cacio e Pepe')

    def test_does_not_display_invalid_recipes_for_that_user(self):
        user = User.objects.create()
        user.save()
        other_user = User()
        other_user.save()
        Recipe.objects.create(title='salmon', url_name='salmon', user=other_user)
        response = self.client.get('/users/%d/recipe/salmon' % user.id)
        self.assertEqual(response.status_code, 404)


class NewUserTest(TestCase):

    def test_save_a_post_request_for_new_user(self):
        self.client.post('/users/new',
                         data={'username': 'ben'})
        self.assertEqual(User.objects.count(), 1)

    def test_redirects_after_a_post(self):
        response = self.client.post('/users/new',
                                    data={'username': 'ben'})
        user = User.objects.first()
        self.assertRedirects(response, '/users/%d/' % user.id)