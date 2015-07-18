from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

import os
import shutil
import requests

class RecipeExportTest(FunctionalTest):

    def test_can_export_a_recipe(self):
        # Ben goes to the recipe website homepage
        self.browser.get(self.server_url)

        # He notices the page title mention cookbook
        self.assertIn('cookbook', self.browser.title)

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

        # When he adds a new recipe, he is taken to a new URL
        self.assertRegex(self.browser.current_url, '/users/.*/add_recipe')

        # He sees a form with a textbox for name, ingredients, directions and servings
        # along with a 'cancel' and 'add' button
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Add Recipe', header_text)
        name_textbox = self.browser.find_element_by_id('id_title')
        self.assertEqual(name_textbox.get_attribute('placeholder'),
                         'Enter the title of the recipe')
        ingredients_textbox = self.browser.find_element_by_id('id_ingredients')
        directions_textbox = self.browser.find_element_by_id('id_directions')
        servings_textbox = self.browser.find_element_by_id('id_servings')
        add_button = self.browser.find_element_by_id('id_add_button')

        # He types in Grilled Halibut with Mango-Avocado Salsa into the textbox for name
        name_textbox.send_keys('Grilled Halibut with Mango-Avocado Salsa')

        # He types in ingredients:
        ingredients_textbox.send_keys('1 medium ripe avocado, peeled and cut into 1/2" dice')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('1 medium ripe mango, peeled and cut into 1/2" dice')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('1 cup cherry tomatoes, quartered')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('4 large fresh basil leaves, thinly sliced')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('3 tablespoons extra-virgin olive oil, divided, plus more for brushing')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('3 tablespoons fresh lime juice, divided')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('Kosher salt and freshly ground black pepper')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('4 6-ounce halibut or mahi-mahi fillets')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('4 lime wedges')

        # He then types in the following for directions:
        directions_textbox.send_keys('Prepare a grill to medium-high heat. Gently combine the avocado, mango, '
                                     'tomatoes, basil, 1 tablespoon oil, and 1 tablespoon lime juice in a large mixing '
                                     'bowl. Season salsa to taste with salt and pepper and set aside at room '
                                     'temperature, gently tossing occasionally.')
        directions_textbox.send_keys(Keys.ENTER)
        directions_textbox.send_keys('Place fish fillets in a 13x9x2" glass baking dish. Drizzle remaining 2 '
                                     'tablespoon oil and 2 tablespoon lime juice over. Season fish with salt and '
                                     'pepper. Let marinate at room temperature for  10 minutes, turning fish '
                                     'occasionally.')
        directions_textbox.send_keys(Keys.ENTER)
        directions_textbox.send_keys('Brush grill rack with oil. Grill fish until just opaque in center, about 5 '
                                     'minutes per side. Transfer to plates. Spoon mango-avocado salsa over fish. '
                                     'Squeeze a lime wedge over each and serve.')

        # He then types in the servings
        servings_textbox.send_keys('4')

        # Finally, he clicks the add button
        add_button.click()

        # He is returned to the main page

        # He sees that the recipe appears in the list of recipes
        self.check_for_row_in_list_table('Grilled Halibut with Mango-Avocado Salsa')

        # He then goes to add another recipe
        add_recipe_button = self.browser.find_element_by_id('id_add_recipe_button')
        add_recipe_button.click()

        # He then goes to add yet another recipe
        # He sees a form with a textbox for name, ingredients, directions and servings
        # along with a 'cancel' and 'add' button
        name_textbox = self.browser.find_element_by_id('id_title')
        add_button = self.browser.find_element_by_id('id_add_button')

        # He types in Grilled Halibut with Mango-Avocado Salsa into the textbox for name
        name_textbox.send_keys('Yogurt-Marinated Grilled Chicken')
        add_button.click()

        # He sees that both recipes appear in the list of recipes
        self.check_for_row_in_list_table('Grilled Halibut with Mango-Avocado Salsa')
        self.check_for_row_in_list_table('Yogurt-Marinated Grilled Chicken')

        # Ben wants to back up his recipes locally to make sure that all the time
        # that he put into curating the recipes does not get lost.

        # He sees there is an export button (TODO: no export button when no recipes?)
        export_button = self.browser.find_element_by_id('id_export_button')

        # He clicks the export button
        # don't actually click, but use wget/requests to get the file
        export_button_url = export_button.get_attribute('href')
        response = requests.get(export_button_url)

        # He receives a zip file
        zip_content = response.content
        with open('/tmp/recipes.zip', 'wb') as f:
            f.write(zip_content)

        # He unzips the file and sees his two recipes
        shutil.unpack_archive('/tmp/recipes.zip', '/tmp')
        self.assertEqual(len(os.listdir('/tmp/recipes')), 2)
        lines = []
        with open('/tmp/recipes/grilled-halibut-with-mango-avocado-salsa') as f:
            lines = f.readlines()

        # He verifies the content of the recipes
        self.assertIn('4 6-ounce halibut or mahi-mahi fillets\n', lines)

        os.remove('/tmp/recipes.zip')
        shutil.rmtree('/tmp/recipes')
