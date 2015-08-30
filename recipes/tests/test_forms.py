from django.test import TestCase

from recipes.forms import RecipeForm


class RecipeFormTest(TestCase):

    def test_form_renders_recipe_text_input(self):
        form = RecipeForm()
        self.assertIn('placeholder="Enter the title of the recipe"', form.as_p())
        self.assertIn('class="form-control"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = RecipeForm(data={'title': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['title'],
            ['This field is required.']
            )
