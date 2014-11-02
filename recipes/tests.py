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
                         data={'recipe_title': 'New recipe'})
        self.assertEqual(Recipe.objects.count(), 1)
        new_recipe = Recipe.objects.first()
        self.assertEqual(new_recipe.title, 'New recipe')
        self.assertEqual(new_recipe.user, user)

    def test_redirects_after_post(self):
        user = User()
        user.save()
        response = self.client.post('/users/%d/add_recipe' % user.id,
                                    data={'recipe_title': 'Caico e pepe'})
        self.assertRedirects(response, '/users/%d/' % user.id)


class UserAndRecipeModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        user = User()
        user.save()

        recipe1 = Recipe()
        recipe1.title = 'cacio e pepe'
        recipe1.ingredients = 'kosher salt\n6 oz. pasta \n3 Tbsp. unsalted butter\n 1 tsp. freshly cracked black pepper'
        recipe1.directions = 'bring water to a boil\ncook pasta\nadd butter and pepper'
        recipe1.servings = '4'
        recipe1.user = user
        recipe1.save()

        recipe2 = Recipe()
        recipe2.title = 'BA Burger Deluxe'
        recipe2.ingredients = '1 1/2 pounds ground chunk\nkosher salt\n4 slices American cheese\n 4 potato rolls'
        recipe2.directions = 'divide meat into 4 equal portions\nBuild a medium-hot fire\nCook for 4 mins, flip then 3'
        recipe2.servings = '4'
        recipe2.user = user
        recipe2.save()

        saved_user = User.objects.first()
        self.assertEqual(saved_user, user)

        saved_items = Recipe.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.title, 'cacio e pepe')
        self.assertEqual(first_saved_item.user, user)
        self.assertEqual(second_saved_item.title, 'BA Burger Deluxe')
        self.assertEqual(second_saved_item.user, user)


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
