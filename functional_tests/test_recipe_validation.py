from unittest import skip
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class RecipeValidationTest(FunctionalTest):

    def test_cannot_add_empty_recipe_title(self):
        # Ben goes to the recipe website homepage
        self.browser.get(self.server_url)

        # He is invited to enter his name to create his own cookbook or
        # view other user's cookbook's
        # Ben wants to create his own right now, so he enters his name
        # and then clicks the 'get started button'
        username_input = self.browser.find_element_by_id('id_username')
        username_input.send_keys('Ben')
        username_input.send_keys(Keys.ENTER)

        # Ben goes to a unique URL which includes his name
        ben_url = self.browser.current_url
        self.assertRegex(ben_url, '/users/ben.+')

        # He is invited to click on a link to add a new recipe
        add_recipe_button = self.browser.find_element_by_id('id_add_recipe_button')
        self.assertIn('Add recipe', add_recipe_button.text)

        # He clicks on the link and new page appears
        add_recipe_button.click()

        # He gets excited and clicks and the add button accidentally
        add_button = self.browser.find_element_by_id('id_add_button')
        add_button.click()

        # He sees an error message saying that the recipe title cannot be
        # be blank
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, 'This field is required.')

        # He fills in the recipe title
        name_textbox = self.browser.find_element_by_id('id_title')
        name_textbox.send_keys('Grilled Halibut with Mango-Avocado Salsa')

        # He tries again
        add_button = self.browser.find_element_by_id('id_add_button')
        add_button.click()

        # Another error for ingredients
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, 'This field is required.')

        # He adds an ingredient
        name_textbox = self.browser.find_element_by_id('id_title')
        name_textbox.send_keys('Grilled Halibut with Mango-Avocado Salsa')

        ingredients_textbox = self.browser.find_element_by_id('id_ingredients')
        ingredients_textbox.send_keys('1 medium ripe avocado, peeled and cut into 1/2" dice')

        # He tries again
        add_button = self.browser.find_element_by_id('id_add_button')
        add_button.click()

        # Another error for directions
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, 'This field is required.')

        # He adds a step
        name_textbox = self.browser.find_element_by_id('id_title')
        name_textbox.send_keys('Grilled Halibut with Mango-Avocado Salsa')

        ingredients_textbox = self.browser.find_element_by_id('id_ingredients')
        ingredients_textbox.send_keys('1 medium ripe avocado, peeled and cut into 1/2" dice')

        directions_textbox = self.browser.find_element_by_id('id_directions')
        directions_textbox.send_keys('Prepare a grill to medium-high heat. Gently combine the avocado, mango, '
                                     'tomatoes, basil, 1 tablespoon oil, and 1 tablespoon lime juice in a large mixing '
                                     'bowl. Season salsa to taste with salt and pepper and set aside at room '
                                     'temperature, gently tossing occasionally.')

        # He tries again
        add_button = self.browser.find_element_by_id('id_add_button')
        add_button.click()

        # Recipe is finally accepted and he is taken back to the main page
        # He sees that the recipe appears in the list of recipes
        self.check_for_row_in_list_table('Grilled Halibut with Mango-Avocado Salsa')
