from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Przejście na stronę główną aplikacji
        self.browser.get('http://localhost:8000')

        # Zwrócenie uwagi, że tytuł strony i nagłówek zawierają słowo 'Rekrutacja'
        self.assertIn('Rekrutacja', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Rekrutacja', header_text)
        self.fail('Zakończenie testu!')

if __name__ == "__main__":
    unittest.main(warnings='ignore')