from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from recipes.views import home, add


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