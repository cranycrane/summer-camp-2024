# test.py
from colorama import Fore, Back, Style, init

import unittest
from game_functions import *

class TestCharacterCreation(unittest.TestCase):
    def test_character_attributes(self):
        # Testování, zda jsou atributy charakteru správně nastaveny
        try:
            character = create_character('Hrdina')
        except NameError as e:
            self.fail(Fore.RED + "Chyba: Zkontroluj, ze mas vsechny promenne definovany: " + str(e))
        

        self.assertIn('name', character, "Chyba: Nebyla definována proměnná 'name'. Musíte vytvořit tuto proměnnou a přiřadit jí hodnotu typu integer.")
        self.assertIn('health', character, "Chyba: Nebyla definována proměnná 'health'. Musíte vytvořit tuto proměnnou a přiřadit jí hodnotu typu integer.")
        self.assertIn('coins', character, "Chyba: Nebyla definována proměnná 'coins'. Musíte vytvořit tuto proměnnou a přiřadit jí hodnotu typu integer.")
        self.assertIn('inventory', character, "Chyba: Nebyla definována proměnná 'inventory'. Musíte vytvořit tuto proměnnou a přiřadit jí hodnotu typu integer.")

        self.assertIsInstance(character, dict, "Funkce by měla vrátit slovník")
        self.assertIsInstance(character['name'], str, "Jméno by mělo být datového typu řetězce.")
        self.assertIsInstance(character['health'], int, "Životy by měly být datového typu integer.")
        self.assertIsInstance(character['coins'], int, "Peníze by měly být datového typu integer")
        self.assertIsInstance(character['inventory'], list, "Inventář by mělo být pole")
        self.assertEqual(len(character['inventory']), 0, "Inventář by měl být prázdný")

if __name__ == '__main__':
    init(autoreset=True)
    unittest.main()
