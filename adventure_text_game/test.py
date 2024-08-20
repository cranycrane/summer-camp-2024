# test.py
from colorama import Fore, Back, Style, init

import unittest
from unittest.mock import patch
from adventure_text_game.adventure import *


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

    @patch('builtins.input', side_effect=[98])  # Neplatný výběr produktu
    def test_trade_invalid_input(self, mock_input):
        trade(self.character)
        self.assertTrue(len(self.character['inventory']) == 0)
        self.assertEqual(self.character['coins'], 150)  # Mince by se neměly změnit

    @patch('random.randrange', side_effect=[50, 45])  # Předpokládáme, že bojové číslo je 50, nepřítel hádá 45
    @patch('builtins.input', return_value='48')  # Hráč hádá 48
    @patch('time.sleep', return_value=None)
    def test_player_wins(self, mock_input, mock_randrange, _):
        fight(self.character)
        self.assertEqual(self.character['coins'], 250)
        self.assertEqual(self.character['health'], 100)

    @patch('random.randrange', side_effect=[50, 49])  # Nepřítel je blíže
    @patch('builtins.input', return_value='30')
    @patch('time.sleep', return_value=None)
    def test_player_loses(self, mock_input, mock_randrange, _):
        try:
            fight(self.character)
        except PlayerDiedException as e:
            self.assertIn("Hráč umřel", str(e))
        self.assertEqual(self.character['coins'], 150)
        self.assertEqual(self.character['health'], 70)

    @patch('random.randrange', side_effect=[50, 48])  # Nerozhodný
    @patch('builtins.input', return_value='48')
    @patch('time.sleep', return_value=None)
    def test_draw(self, mock_input, mock_randrange, _):
        fight(self.character)
        self.assertEqual(self.character['health'], 100)

    @patch('random.randrange', side_effect=[50, 60])  # Neplatný vstup, hra přečte 50
    @patch('builtins.input', return_value='101')
    @patch('time.sleep', return_value=None)
    def test_fight_invalid_input(self, mock_input, mock_randrange, _):
        fight(self.character)
        self.assertEqual(self.character['coins'], 150)  # Zůstávají stejné
        self.assertEqual(self.character['health'], 100)  # Žádná změna

if __name__ == '__main__':
    init(autoreset=True)
    result = unittest.main(exit=False)
    if result.result.wasSuccessful():
        print(Fore.GREEN + "Všechny úkoly splněny! Skvělá práce!")
    else:
        print(Fore.RED + f"Některé úkoly nejsou splněné. Zbývá splnit {len(result.result.failures)} úkolů.")
