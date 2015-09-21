from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class RecipeImportTest(FunctionalTest):

    def test_can_import_a_recipe(self):
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

        # He sees a button for importing
        import_textbox = self.browser.find_element_by_id('id_import_url')
        import_button = self.browser.find_element_by_id('id_import_button')

        # He inputs a website and clicks the import button
        import_textbox.send_keys('http://www.bonappetit.com/recipe/gwyneth-paltrow-s-grilled-halibut-with-mango-avocado-salsa')
        import_button.click()

        # Finally, he clicks the add button
        add_button.click()

        # He is returned to the main page

        # He sees that the recipe appears in the list of recipes
        self.check_for_row_in_list_table('Grilled Halibut with Mango-Avocado Salsa')

        # He clicks on the recipe that he just added to verify the content
        recipe_link = self.browser.find_element_by_link_text('Grilled Halibut with Mango-Avocado Salsa')
        recipe_link.click()
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('4 6-ounce halibut or mahi-mahi fillets', page_text)
