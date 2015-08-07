from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class RecipeEditTest(FunctionalTest):

    def test_can_add_a_recipe(self):
        # Ben goes to the recipe website homepage
        self.browser.get(self.server_url)

        # He notices the page title mention cookbook
        self.assertIn('cookbook', self.browser.title)

        # He is invited to enter his name to create his own cookbook or
        # view other user's cookbook's
        # Ben wants to create his own right now, so he enters his name
        # and then clicks the 'get started button'
        # TODO -- duplication here. consider refactoring if there is a third instance
        username_input = self.browser.find_element_by_id('id_username')
        username_input.send_keys('ben')
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
        servings_textbox.send_keys('7')

        # Finally, he clicks the add button
        add_button.click()

        # He is returned to the main page

        # He sees that the recipe appears in the list of recipes
        self.check_for_row_in_list_table('Grilled Halibut with Mango-Avocado Salsa')

        # Ben then clicks on a recipe to get the full info
        recipe_link = self.browser.find_element_by_link_text('Grilled Halibut with Mango-Avocado Salsa')
        recipe_link.click()

        # He is taken to a new page which has the title in the url
        self.assertRegex(self.browser.current_url, '/users/(\S+)/recipe/grilled-halibut-with-mango-avocado-salsa')

        # The new page lists all of the ingredients and directions
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('1 medium ripe avocado, peeled and cut into 1/2" dice', page_text)
        self.assertIn('Prepare a grill to medium-high heat. Gently combine the avocado, mango, ', page_text)

        # He then remembers that the servings are for 8 people and a chili pepper is needed. He clicks
        # on the edit button to start editing
        edit_button = self.browser.find_element_by_id('id_edit_button')
        self.assertIn('Edit', edit_button.text)
        edit_button.click()

        # The edit page shows the same text as before
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('1 medium ripe avocado, peeled and cut into 1/2" dice', page_text)
        self.assertIn('Prepare a grill to medium-high heat. Gently combine the avocado, mango, ', page_text)

        # He changes the number of servings from 7 to 8
        servings_textbox = self.browser.find_element_by_id('id_servings')
        servings_textbox.send_keys(Keys.BACKSPACE)
        servings_textbox.send_keys('8')

        # He adds chili pepper to the list of ingredients
        ingredients_textbox = self.browser.find_element_by_id('id_ingredients')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('1 chili pepper')

        # He adds a note for next time
        notes_textbox = self.browser.find_element_by_id('id_notes')
        notes_textbox.send_keys("Wasn't that spicy, added a pepper")

        # He then clicks the save button
        save_button = self.browser.find_element_by_id('id_save_button')
        self.assertIn('Save', save_button.text)
        save_button.click()

        # He is returned to the recipe page
        self.assertRegex(self.browser.current_url, '/users/(\S+)/recipe/grilled-halibut-with-mango-avocado-salsa')

        # He can see his changes reflected on the page
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('8', page_text)
        self.assertNotIn('7', page_text)
        self.assertIn('1 chili pepper', page_text)
        self.assertIn('added a pepper', page_text)

        #self.fail('Finish the test')
        # He changes his mind and cancels
        # cancel_button = self.browser.find_element_by_name('id_cancel_button')
        #cancel_button.click()

        # He is returned to the main page

        # The number of recipes is still 1
        # table = self.browser.find_element_by_id('id_recipe_table')
        # rows = table.find_element_by_tag_name('tr')
        #self.assertEqual(len(rows), 1)
