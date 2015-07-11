from django.test import TestCase

from recipes.models import Recipe, User


class UserModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        user = User()
        user.name = 'Sarah'
        user.save()

        saved_user = User.objects.first()
        self.assertEqual(saved_user, user)
        self.assertEqual(saved_user.name, 'Sarah')


class RecipeModelTest(TestCase):

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


