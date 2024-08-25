# test.py
from colorama import Fore, Back, Style, init

import unittest
import io
import sys
from unittest.mock import patch
from adventure_student import *


class TestcharakterCreation(unittest.TestCase):
    def setUp(self):
        # Vytvoříme zkušební postavu pro použití ve všech testech
        self.charakter = {
            'jméno': 'Hrdina',
            'životy': 100,
            'peníze': 150,
            'inventář': []
        }


    @patch('builtins.input', side_effect=[''])
    def test_get_charakter_name_invalid(self, mock_input):
        charakter_name = získej_jméno_charaktera()
        self.assertIsInstance(charakter_name, str, Fore.RED + "Jméno by mělo být datového typu řetězce.")
        self.assertNotEqual(len(charakter_name), 0, Fore.RED + 'Jméno charaktera nesmí být prázdné - mít délku 0')

    @patch('builtins.input', side_effect=['Hrdina'])
    def test_charakter_attributes(self, mock_input):
        # Testování, zda jsou atributy charakteru správně nastaveny
        try:
            charakter = vytvoř_charakter()
        except NameError as e:
            self.fail(Fore.RED + "Chyba: Zkontroluj, ze mas vsechny promenne definovany: " + str(e))
        

        self.assertIn('jméno', charakter, Fore.RED + "Chyba: Nebyla definována proměnná 'jméno'. Musíte vytvořit tuto proměnnou a přiřadit jí hodnotu typu integer.")
        self.assertIn('životy', charakter, Fore.RED + "Chyba: Nebyla definována proměnná 'životy'. Musíte vytvořit tuto proměnnou a přiřadit jí hodnotu typu integer.")
        self.assertIn('peníze', charakter, Fore.RED + "Chyba: Nebyla definována proměnná 'peníze'. Musíte vytvořit tuto proměnnou a přiřadit jí hodnotu typu integer.")
        self.assertIn('inventář', charakter, Fore.RED + "Chyba: Nebyla definována proměnná 'inventář'. Musíte vytvořit tuto proměnnou a přiřadit jí hodnotu typu integer.")

        self.assertIsInstance(charakter, dict, Fore.RED + "Funkce by měla vrátit slovník")
        self.assertIsInstance(charakter['jméno'], str, Fore.RED + "Jméno by mělo být datového typu řetězce.")
        self.assertIsInstance(charakter['životy'], int, Fore.RED + "Životy by měly být datového typu integer.")
        self.assertIsInstance(charakter['peníze'], int, Fore.RED + "Peníze by měly být datového typu integer")
        self.assertIsInstance(charakter['inventář'], list, Fore.RED + "Inventář by mělo být pole")
        self.assertEqual(len(charakter['inventář']), 0, Fore.RED + "Inventář by měl být prázdný")


    def test_print_info(self):
        captured_output = io.StringIO()          # Vytvoření StringIO objektu
        sys.stdout = captured_output             # Přesměrování stdout
        
        zobraz_informace_charakteru(self.charakter)
        
        sys.stdout = sys.__stdout__
        
        self.assertIn('Životy', captured_output.getvalue(), Fore.RED + 'Ve výstupu funkce chybí "Životy"')
        self.assertIn('100', captured_output.getvalue(), Fore.RED + 'Ve výstupu funkce chybí "100"')
        self.assertIn('Peníze', captured_output.getvalue(), Fore.RED + 'Ve výstupu funkce chybí "Peníze"')
        self.assertIn('150', captured_output.getvalue(), Fore.RED + 'Ve výstupu funkce chybí "150"')

    @patch('builtins.input', side_effect=[1])  # Simulace vstupu uživatele
    def test_valid_purchase(self, mock_input):
        obchodovat(self.charakter)
        self.assertIn('Život', self.charakter['inventář'])
        self.assertEqual(self.charakter['peníze'], 100)  # 150 - 50 cena za život

    @patch('builtins.input', side_effect=[1])  # Simulace nákupu životu, který stojí 50 mincí
    def test_purchase_with_insufficient_coins(self, mock_input):
        self.charakter['peníze'] = 30  # Nastavení malého počtu mincí
        obchodovat(self.charakter)
        self.assertNotIn('Život', self.charakter['inventář'])
        self.assertEqual(self.charakter['peníze'], 30)  # Mince by se neměly změnit

    @patch('builtins.input', side_effect=[98])  # Neplatný výběr produktu
    def test_trade_invalid_input(self, mock_input):
        obchodovat(self.charakter)
        self.assertTrue(len(self.charakter['inventář']) == 0)
        self.assertEqual(self.charakter['peníze'], 150)  # Mince by se neměly změnit

    @patch('builtins.input', side_effect=[1])  # Simulace nákupu životu, který stojí 50 mincí
    def test_trade_output(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output        
        
        obchodovat(self.charakter)
        
        sys.stdout = sys.__stdout__
        self.assertIn('Život', captured_output.getvalue(), Fore.RED + 'Ve výstupu funkce chybí "Život"')
        self.assertIn('100', captured_output.getvalue(), Fore.RED + 'Ve výstupu funkce chybí počet zbývajících mincí')



    @patch('random.randrange', side_effect=[50, 45])  # Předpokládáme, že bojové číslo je 50, nepřítel hádá 45
    @patch('builtins.input', return_value='48')  # Hráč hádá 48
    @patch('time.sleep', return_value=None)
    def test_player_wins(self, mock_input, mock_randrange, _):
        bojovat(self.charakter)
        self.assertEqual(self.charakter['peníze'], 250)
        self.assertEqual(self.charakter['životy'], 100)

    @patch('random.randrange', side_effect=[50, 49])  # Nepřítel je blíže
    @patch('builtins.input', return_value='30')
    @patch('time.sleep', return_value=None)
    def test_player_loses(self, mock_input, mock_randrange, _):
        try:
            bojovat(self.charakter)
        except PlayerDiedException as e:
            self.assertIn("Hráč umřel", str(e))
        self.assertEqual(self.charakter['peníze'], 150)
        self.assertEqual(self.charakter['životy'], 70)

    @patch('random.randrange', side_effect=[50, 48])  # Nerozhodný
    @patch('builtins.input', return_value='48')
    @patch('time.sleep', return_value=None)
    def test_draw(self, mock_input, mock_randrange, _):
        bojovat(self.charakter)
        self.assertEqual(self.charakter['životy'], 100)

    @patch('random.randrange', side_effect=[50, 60])  # Neplatný vstup, hra přečte 50
    @patch('builtins.input', return_value='101')
    @patch('time.sleep', return_value=None)
    def test_fight_invalid_input(self, mock_input, mock_randrange, _):
        bojovat(self.charakter)
        self.assertEqual(self.charakter['peníze'], 150)  # Zůstávají stejné
        self.assertEqual(self.charakter['životy'], 100)  # Žádná změna

if __name__ == '__main__':
    init(autoreset=True)
    result = unittest.main(exit=False)
    if result.result.wasSuccessful():
        print(Fore.GREEN + "Všechny úkoly splněny! Skvělá práce!")
    else:
        print(Fore.RED + f"Některé úkoly nejsou splněné. Zbývá splnit {len(result.result.failures)} úkolů.")
