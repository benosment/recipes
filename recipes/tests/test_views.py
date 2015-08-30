from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from recipes.views import home
from recipes.models import Recipe, User
from recipes.forms import RecipeForm


class HomeTest(TestCase):

    def test_root_url_resolves_to_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class NewRecipeTest(TestCase):

    def test_add_recipe_page_uses_recipe_form(self):
        user = User()
        user.name = 'ben'
        user.save()
        response = self.client.get('/users/%s/add_recipe' % user.name)
        self.assertIsInstance(response.context['form'], RecipeForm)


    def test_save_a_post_request_for_an_existing_user(self):
        user = User()
        user.name = 'ben'
        user.save()
        self.client.post('/users/%s/add_recipe' % user.name,
                         data={'title': 'new recipe',
                               'ingredients': 'pepper',
                               'directions': 'mix'})
        self.assertEqual(Recipe.objects.count(), 1)
        new_recipe = Recipe.objects.first()
        self.assertEqual(new_recipe.title, 'new recipe')
        self.assertEqual(new_recipe.user, user)

    def test_redirects_after_post(self):
        user = User()
        user.name = 'ben'
        user.save()
        response = self.client.post('/users/%s/add_recipe' % user.name,
                                    data={'title': 'Caico e pepe',
                                          'ingredients': 'pepper',
                                          'directions': 'mix'})
        self.assertRedirects(response, '/users/%s/' % user.name)

    def test_validation_errors_appear(self):
        user = User()
        user.name = 'ben'
        user.save()
        response = self.client.post('/users/%s/add_recipe' % user.name,
                                    data={'title': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add.html')
        expected_error = 'You have to specify a recipe name.'
        #self.assertContains(response.content, expected_error)

    def test_verify_invalid_items_are_not_saved(self):
        user = User()
        user.name = 'ben'
        user.save()
        self.client.post('/users/%s/add_recipe' % user.name,
                         data={'title': ''})
        self.assertEqual(Recipe.objects.count(), 0)


class EditRecipeTest(TestCase):

    def test_save_a_post_request_for_an_existing_recipe(self):
        user = User()
        user.name = 'ben'
        user.save()

        recipe = Recipe()
        recipe.title = 'cacio e pepe'
        recipe.url_name = 'cacio-e-pepe'
        recipe.ingredients = 'kosher salt\n6 oz. pasta \n3 Tbsp. unsalted butter\n 1 tsp. freshly cracked black pepper'
        recipe.directions = 'bring water to a boil\ncook pasta\nadd butter and pepper'
        recipe.servings = '4'
        recipe.user = user
        recipe.save()

        self.client.post('/users/%s/recipe/%s/edit' % (user.name, recipe.url_name),
                         data={'title': 'Cacio e Pepe'})

        edited_recipe = Recipe.objects.first()
        self.assertEqual(edited_recipe.title, 'Cacio e Pepe')

    def test_redirects_after_save(self):
        user = User()
        user.name = 'ben'
        user.save()

        recipe = Recipe()
        recipe.title = 'cacio e pepe'
        recipe.url_name = 'cacio-e-pepe'
        recipe.ingredients = 'kosher salt\n6 oz. pasta \n3 Tbsp. unsalted butter\n 1 tsp. freshly cracked black pepper'
        recipe.directions = 'bring water to a boil\ncook pasta\nadd butter and pepper'
        recipe.servings = '4'
        recipe.user = user
        recipe.save()

        response = self.client.post('/users/%s/recipe/%s/edit' % (user.name, recipe.url_name),
                                    data={'title': 'Cacio e Pepe'})
        self.assertRedirects(response, '/users/%s/recipe/%s' % (user.name, recipe.url_name))


class UserViewTest(TestCase):

    def test_uses_user_template(self):
        user = User.objects.create()
        user.name = 'ben'
        user.save()
        response = self.client.get('/users/%s/' % user.name)
        self.assertTemplateUsed(response, 'user.html')

    def test_displays_only_recipes_for_that_user(self):
        correct_user = User()
        correct_user.name = 'bill'
        correct_user.save()
        other_user = User()
        other_user.name = 'ted'
        other_user.save()
        Recipe.objects.create(title='cacio e pepe', user=correct_user)
        Recipe.objects.create(title='BA Burger Deluxe', user=correct_user)
        Recipe.objects.create(title='salmon', user=other_user)
        Recipe.objects.create(title='tuna burger', user=other_user)

        response = self.client.get('/users/%s/' % correct_user.name)

        self.assertContains(response, 'cacio e pepe')
        self.assertContains(response, 'BA Burger Deluxe')
        self.assertNotContains(response, 'salmon')
        self.assertNotContains(response, 'tuna burger')

    def test_passes_correct_user_to_template(self):
        user = User.objects.create()
        user.name = 'steve'
        user.save()
        other_user = User.objects.create()
        response = self.client.get('/users/%s/' % (user.name,))
        self.assertEqual(response.context['user'], user)


class RecipeViewTest(TestCase):

    def test_uses_recipe_template(self):
        user = User.objects.create()
        user.name = 'ben'
        user.save()
        Recipe.objects.create(title='cacio e pepe', url_name='cacio-e-pepe', user=user)
        response = self.client.get('/users/%s/recipe/cacio-e-pepe' % user.name)
        self.assertTemplateUsed(response, 'recipe.html')

    def test_passes_correct_recipe_to_template(self):
        user = User.objects.create()
        user.name = 'ben'
        user.save()
        recipe = Recipe.objects.create(title='cacio e pepe', url_name='cacio-e-pepe', user=user)
        response = self.client.get('/users/%s/recipe/cacio-e-pepe' % user.name.lower())
        self.assertEqual(response.context['recipe'], recipe)

    def test_displays_valid_recipes_for_that_user(self):
        user = User.objects.create()
        user.name = 'ben'
        user.save()
        Recipe.objects.create(title='Cacio e Pepe', url_name='cacio-e-pepe', user=user)
        response = self.client.get('/users/%s/recipe/cacio-e-pepe' % user.name.lower())
        self.assertContains(response, 'Cacio e Pepe')

    def test_does_not_display_invalid_recipes_for_that_user(self):
        user = User.objects.create()
        user.name = 'ben'
        user.save()
        other_user = User()
        other_user.save()
        Recipe.objects.create(title='salmon', url_name='salmon', user=other_user)
        response = self.client.get('/users/%s/recipe/salmon' % user.name.lower())
        self.assertEqual(response.status_code, 404)


class NewUserTest(TestCase):

    def test_save_a_post_request_for_new_user(self):
        self.client.post('/',
                         data={'user_name': 'Ben'})
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.display_name, 'Ben')
        self.assertEqual(user.name, 'ben')

    def test_redirects_after_a_post(self):
        response = self.client.post('/',
                                    data={'user_name': 'Ben'})
        user = User.objects.first()
        self.assertRedirects(response, '/users/%s/' % user.name)
