# test.py
from colorama import Fore, Back, Style, init

import unittest
from unittest.mock import patch
from game_functions import *

class TestCharacterCreation(unittest.TestCase):
    def setUp(self):
        # Vytvoříme zkušební postavu pro použití ve všech testech
        self.character = {
            'name': 'Hrdina',
            'health': 100,
            'coins': 150,
            'inventory': []
        }

    @patch('builtins.input', side_effect=[''])
    def test_get_character_name_invalid(self, mock_input):
        character_name = get_character_name()
        self.assertIsInstance(character_name, str, Fore.RED + "Jméno by mělo být datového typu řetězce.")
        self.assertNotEqual(len(character_name), 0, Fore.RED + 'Jméno charaktera nesmí být prázdné - mít délku 0')

    @patch('builtins.input', side_effect=['Hrdina'])
    def test_character_attributes(self, mock_input):
        # Testování, zda jsou atributy charakteru správně nastaveny
        try:
            character = create_character()
        except NameError as e:
            self.fail(Fore.RED + "Chyba: Zkontroluj, ze mas vsechny promenne definovany: " + str(e))
        

        self.assertIn('name', character, Fore.RED + "Chyba: Nebyla definována proměnná 'name'. Musíte vytvořit tuto proměnnou a přiřadit jí hodnotu typu integer.")
        self.assertIn('health', character, Fore.RED + "Chyba: Nebyla definována proměnná 'health'. Musíte vytvořit tuto proměnnou a přiřadit jí hodnotu typu integer.")
        self.assertIn('coins', character, Fore.RED + "Chyba: Nebyla definována proměnná 'coins'. Musíte vytvořit tuto proměnnou a přiřadit jí hodnotu typu integer.")
        self.assertIn('inventory', character, Fore.RED + "Chyba: Nebyla definována proměnná 'inventory'. Musíte vytvořit tuto proměnnou a přiřadit jí hodnotu typu integer.")

        self.assertIsInstance(character, dict, Fore.RED + "Funkce by měla vrátit slovník")
        self.assertIsInstance(character['name'], str, Fore.RED + "Jméno by mělo být datového typu řetězce.")
        self.assertIsInstance(character['health'], int, Fore.RED + "Životy by měly být datového typu integer.")
        self.assertIsInstance(character['coins'], int, Fore.RED + "Peníze by měly být datového typu integer")
        self.assertIsInstance(character['inventory'], list, Fore.RED + "Inventář by mělo být pole")
        self.assertEqual(len(character['inventory']), 0, Fore.RED + "Inventář by měl být prázdný")

    @patch('builtins.input', side_effect=[1])  # Simulace vstupu uživatele
    def test_valid_purchase(self, mock_input):
        trade(self.character)
        self.assertIn('Život', self.character['inventory'])
        self.assertEqual(self.character['coins'], 100)  # 150 - 50 cena za život

    @patch('builtins.input', side_effect=[1])  # Simulace nákupu životu, který stojí 50 mincí
    def test_purchase_with_insufficient_coins(self, mock_input):
        self.character['coins'] = 30  # Nastavení malého počtu mincí
        trade(self.character)
        self.assertNotIn('Život', self.character['inventory'])
        self.assertEqual(self.character['coins'], 30)  # Mince by se neměly změnit

    @patch('builtins.input', side_effect=[99])  # Neplatný výběr produktu
    def test_invalid_input(self, mock_input):
        trade(self.character)
        self.assertTrue(len(self.character['inventory']) == 0)
        self.assertEqual(self.character['coins'], 150)  # Mince by se neměly změnit



if __name__ == '__main__':
    init(autoreset=True)
    unittest.main()
