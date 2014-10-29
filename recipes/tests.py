from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from recipes.views import home
from recipes.models import Recipe


class HomeTest(TestCase):

    def test_root_url_resolves_to_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


# class NewRecipeTest(TestCase):
#
#     def test_save_a_post_request_for_new_recipe(self):
#         self.client.post('/users/ben/recipes/new',
#                          data={'recipe_title': 'New recipe'})
#         self.assertEqual(Recipe.objects.count(), 1)
#         new_recipe = Recipe.objects.first()
#         self.assertEqual(new_recipe.title, 'New recipe')
#
#     def test_redirects_after_post(self):
#         response = self.client.post('/users/ben/recipes/new',
#                                     data={'recipe_title': 'Caico e pepe'})
#         self.assertRedirects(response, '/users/ben/recipes/caico-e-pepe')


class RecipeModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        recipe1 = Recipe()
        recipe1.title = 'cacio e pepe'
        recipe1.ingredients = 'kosher salt\n6 oz. pasta \n3 Tbsp. unsalted butter\n 1 tsp. freshly cracked black pepper'
        recipe1.directions = 'bring water to a boil\ncook pasta\nadd butter and pepper'
        recipe1.servings = '4'
        recipe1.save()

        recipe2 = Recipe()
        recipe2.title = 'BA Burger Deluxe'
        recipe2.ingredients = '1 1/2 pounds ground chunk\nkosher salt\n4 slices American cheese\n 4 potato rolls'
        recipe2.directions = 'divide meat into 4 equal portions\nBuild a medium-hot fire\nCook for 4 mins, flip then 3'
        recipe2.servings = '4'
        recipe2.save()

        saved_items = Recipe.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.title, 'cacio e pepe')
        self.assertEqual(second_saved_item.title, 'BA Burger Deluxe')


class UserViewTest(TestCase):

    def test_uses_user_template(self):
        response = self.client.get('/users/ben/')
        self.assertTemplateUsed(response, 'user.html')

    def test_displays_all_recipes(self):
        Recipe.objects.create(title='cacio e pepe')
        Recipe.objects.create(title='BA Burger Deluxe')

        response = self.client.get('/users/ben/')

        self.assertContains(response, 'cacio e pepe')
        self.assertContains(response, 'BA Burger Deluxe')


class NewUserTest(TestCase):

    # def test_save_a_post_request_for_new_user(self):
    #     self.client.post('/users/new',
    #                      data={'username': 'ben'})
    #     self.assertEqual(User.objects.count(), 1)
    #     new_user = User.objects.first()
    #     self.assertEqual(new_user.name, 'ben')

    def test_redirects_after_a_post(self):
        response = self.client.post('/users/new',
                                    data={'username': 'ben'})
        self.assertRedirects(response, '/users/ben/')
