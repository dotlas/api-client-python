import unittest
from unittest.mock import patch, MagicMock
from typing import List
from dotlas import App

class TestApp(unittest.TestCase):  # Replace App with the actual class name

    @classmethod
    def setUpClass(cls):
        cls.app = App("xyz")  # Replace App with the actual class name

    @patch.object(App, "_App__generic_fetch")  # Replace App with the actual class name
    def test_list_commercial_types(self, mock_fetch):
        mock_fetch.return_value = ['retail', 'restaurants', 'gyms']
        result = self.app.list_commercial_types()
        self.assertEqual(result, ['retail', 'restaurants', 'gyms'])

    @patch.object(App, "_App__generic_fetch")  # Replace App with the actual class name
    def test_list_cities(self, mock_fetch):
        mock_fetch.return_value = ['Los Angeles', 'New York', 'Chicago']
        result = self.app.list_cities()
        self.assertEqual(result, ['Los Angeles', 'New York', 'Chicago'])

    @patch.object(App, "_App__generic_fetch")  # Replace App with the actual class name
    def test_list_places_in_city(self, mock_fetch):
        mock_fetch.return_value = ['Burbank', 'Beverly Hills']
        result = self.app.list_places_in_city('Los Angeles')
        self.assertEqual(result, ['Burbank', 'Beverly Hills'])

    @patch.object(App, "_App__generic_fetch")  # Replace App with the actual class name
    def test_list_areas_in_city(self, mock_fetch):
        mock_fetch.return_value = ['Financial District', 'Upper West Side']
        result = self.app.list_areas_in_city('New York')
        self.assertEqual(result, ['Financial District', 'Upper West Side'])

if __name__ == '__main__':
    unittest.main()