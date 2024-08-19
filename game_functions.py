"""
Knihovny: unittest, coloroma


"""
from colorama import Fore, Back, Style

def create_character(character_name):
    # Vytvoření proměnných pro jméno postavy, zdraví, sílu a inventář
    health = 100  # Číslo
    coins = 0  # Číslo
    inventory = []  # Pole/Seznam/List

    # Vracíme slovník, který reprezentuje postavu
    return {
        "name": character_name,
        "health": health,
        "coins": coins,
        "inventory": inventory
    }


def intro():
    print("Vítejte ve hře! Jak se jmenuješ?")
    character_name = input("Zadej jméno: ")
    print(f"Ahoj, {character_name}, tvé dobrodružství začíná...")
    # Zavoláme funkci
    character = create_character(character_name)
    # Vypíšeme informace o charakteru:
    print(f"Jméno: {character_name}, Životů: {character["health"]}, Peněz: {character["coins"]}, Počet itemů v inventáři: {len(character["inventory"])}")



def get_player_choice():
    return input("Co chceš dělat? (např. 'prozkoumat', 'mluvit', 'bojovat', 'quit'): ")

def process_action(action):
    if action == 'prozkoumat':
        explore()
    elif action == 'mluvit':
        talk()
    elif action == 'bojovat':
        fight()
    else:
        print("Neznámá akce.")

def explore():
    # nakupovani
    print("Prozkoumáváš oblast.")

def trade():
    pass

def talk():
    print("Mluvíš s postavou.")

def fight():
    print("Bojuješ s nepřítelem.")

def outro():
    print("Konec hry. Díky za hraní!")
