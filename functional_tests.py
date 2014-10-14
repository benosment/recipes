import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewRecipeTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_add_a_recipe(self):
        # Ben goes to the recipe website homepage
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention cookbook
        self.assertIn('cookbook', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('cookbook', header_text)

        # He is invited to click on a link to add a new recipe
        add_link = self.browser.find_element_by_link_text('add recipe')
        self.assertIn('add recipe', add_link.text)

        # He clicks on the link and new page appears
        add_link.click()

        # He sees a form with a textbox for name, ingredients, directions and servings
        # along with a 'cancel' and 'add' button
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('add recipe', header_text)
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

        # He sees that the recipe appears in the list of cookbook
        table = self.browser.find_element_by_id('id_recipe_table')
        rows = table.find_elements_by_tag_name('tr')
        row_text = [row.text for row in rows]
        self.assertIn('Grilled Halibut with Mango-Avocado Salsa', row_text)

        self.fail('Finish the test')

        # He closes his browser

        # He then reopens his browser and sees that the recipe that he added is still there

        # He then goes to add another recipe
        # add_link = self.browser.find_element_by_link_text('add recipe')
        # add_link.click()

        # He changes his mind and cancels
        # cancel_button = self.browser.find_element_by_name('id_cancel_button')
        #cancel_button.click()

        # He is returned to the main page

        # The number of recipes is still 1
        # table = self.browser.find_element_by_id('id_recipe_table')
        # rows = table.find_element_by_tag_name('tr')
        #self.assertEqual(len(rows), 1)

        # TODO -- add a second recipe
        # TODO -- click on a recipe takes you to the recipe page, verify info
        # TODO -- edit a recipe


if __name__ == '__main__':
    unittest.main(warnings='ignore')
