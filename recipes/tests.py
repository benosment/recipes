from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from recipes.views import home, add
from recipes.models import Recipe


class HomeTest(TestCase):

    def test_root_url_resolves_to_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_returns_correct_html(self):
        request = HttpRequest()
        response = home(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


class AddTest(TestCase):

    def test_add_page_can_save_a_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['recipe_title'] = 'chorizo'

        response = add(request)

        self.assertIn('chorizo', response.content.decode())
        expected_html = render_to_string('home.html',
                                         {'recipe_title': 'chorizo'})
        self.assertEqual(response.content.decode(), expected_html)


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