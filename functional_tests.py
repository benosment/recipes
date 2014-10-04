from selenium import webdriver
import unittest


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
        self.fail('Finish the test')

        # He is invited to click on a link to add a new recipe

        # He clicks on the link and new page appears

        # He sees a form with a textbox for name, ingredients, directions and servings
        # along with a 'cancel' and 'add' button

        # He types in Grilled Halibut with Mango-Avocado Salsa into the textbox for name

        # He types in the following for ingredients:
        #
        # - 1 medium ripe avocado, peeled and cut into 1/2" dice
        # - 1 medium ripe mango, peeled and cut into 1/2" dice
        # - 1 cup cherry tomatoes, quartered
        # - 4 large fresh basil leaves, thinly sliced
        # - 3 tablespoons extra-virgin olive oil, divided, plus more for brushing
        # - 3 tablespoons fresh lime juice, divided
        # - Kosher salt and freshly ground black pepper
        # - 4 6-ounce halibut or mahi-mahi fillets
        # - 4 lime wedges

        # He then types in the following for directions:
        #
        # 1. Prepare a grill to medium-high heat. Gently combine the avocado, mango, tomatoes, basil, 1 tablespoon oil, and
        # 1 tablespoon lime juice in a large mixing bowl. Season salsa to taste with salt and pepper and set aside at room
        # temperature, gently tossing occasionally.
        #
        # 2. Place fish fillets in a 13x9x2" glass baking dish. Drizzle remaining 2 tablespoon oil and 2 tablespoon lime juice
        # over. Season fish with salt and pepper. Let marinate at room temperature for  10 minutes, turning fish occasionally.
        #
        # 3. Brush grill rack with oil. Grill fish until just opaque in center, about 5 minutes per side. Transfer to plates.
        # Spoon mango-avocado salsa over fish. Squeeze a lime wedge over each and serve.


        # He then types in the following for servings

        # Finally, he clicks the add button

        # He is returned to the main page

        # He sees that the recipe appears in the list of cookbook

        # He closes his browser

        # He then reopens his browser and sees that the recipe that he added is still there

        # TODO -- add a second recipe
        # TODO -- click on a recipe takes you to the recipe page, verify info
        # TODO -- edit a recipe


if __name__ == '__main__':
    unittest.main(warnings='ignore')