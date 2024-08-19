from colorama import Fore, Back, Style
import random
import sys
import time
"""
Knihovny: unittest, coloroma
"""


def create_character():
    # Vytvoření proměnných pro jméno postavy, zdraví, peníze a inventář

    health = 100  # Číslo
    coins = 0  # Číslo
    inventory = []  # Pole/Seznam/List

    # Vracíme slovník, který reprezentuje postavu
    return {
        "name": get_character_name(),
        "health": health,
        "coins": coins,
        "inventory": inventory
    }

def get_character_name() -> str:
    """
    Zeptá se hráče, jaké chce mít jméno charakteru a pozdraví ho

    Returns:
        str: Jméno charakteru zadané uživatelem
    """

    character_name = input("Zadej jméno: ")
    
    if len(character_name) == 0:
        print(Fore.RED + "Chyba: Název charakteru nesmí být prázdný")
        character_name = 'Hrdina'

    print(f"Ahoj, {character_name}, tvé dobrodružství začíná...")
    return character_name

def get_player_choice(character) -> str:
    """
    Zeptá se hráče, jakou chce provést akci a vypíše základní informace o charakteru

    Parameters:
    character (dict): Slovník obsahující informace o postavě, včetně mincí a inventáře.
    """

    print("-----------------------------------------------------------------------")
    print(Fore.RED + f"Životy: {character['health']}" )
    print(Fore.BLUE + f"Peníze: {character['coins']}" )
    print("-----------------------------------------------------------------------")

    return input("Co chceš dělat? (např. 'prozkoumat', 'mluvit', 'bojovat', 'obchodovat', 'quit'): ")

def process_action(action, character):
    """
    Zavolá odpovídající funkci dle typu akce

    Parameters:
    action (str): Řetězec obsahující název akce
    character (dict): Slovník obsahující informace o postavě, včetně mincí a inventáře.
    """

    if action == 'prozkoumat':
        explore(character)
    elif action == 'obchodovat':
        trade(character)
    elif action == 'mluvit':
        talk(character)
    elif action == 'bojovat':
        fight(character)
    else:
        print("Neznámá akce.")

def explore(character):
    print("Prozkoumáváš okolí...")

    time.sleep(2)

    discoveries = ["starý meč", "zlatá mince", "magický amulet", "nic"]

    found_item = random.choice(discoveries)
    
    if found_item != "nic":
        character['inventory'].append(found_item)
        print(Fore.GREEN + f"Našel jsi {found_item}!")
    else:
        print(Fore.LIGHTBLACK_EX + "Prozkoumal jsi oblast, ale nenašel jsi nic zajímavého.")

def trade(character):
    """
    Umožňuje hráči nakupovat předměty.

    Parameters:
    character (dict): Slovník obsahující informace o postavě, včetně mincí a inventáře.
    """
    items_for_sale = [
        {'name': 'Život', 'price': 50},
        {'name': 'Síla', 'price': 75},
        {'name': 'Kouzelný lektvar', 'price': 100}
    ]
    
    # Zobrazení dostupných předmětů a jejich cen
    print(Fore.LIGHTMAGENTA_EX +  "Dostupné předměty k nákupu:")
    for index, item in enumerate(items_for_sale):
        print(f"({index + 1}) {item['name']} - Cena: {item['price']} mincí")
    
    # Získání uživatelského vstupu
    product_index = int(input("Co chceš nakoupit? (Vyber číslo): ")) - 1
    print(f"product_index: {product_index}")
    if product_index < 0 or product_index >= len(items_for_sale):
        print(Fore.RED +  "Neplatný výběr.")
        return

    product = items_for_sale[product_index]

    # Kontrola, zda má hráč dost mincí
    if character['coins'] < product['price']:
        print(Fore.RED + "Nemáš dost mincí na koupi tohoto předmětu.")
        return

    # Provedení nákupu
    character['coins'] -= product['price']
    character['inventory'].append(product['name'])
    print(f"Zakoupil jsi {product['name']}. Zbývající mince: {character['coins']}.")


def talk(character):
    print("Mluvíš s postavou.")

def fight(character):
    """
    Boj s příšerou na základě hádání čísla od 0 po 100.
    Příšera hadá taky. Ten kdo uhodne blíž, vyhrává.

    Parameters:
    character (dict): Slovník obsahující informace o postavě, včetně mincí a inventáře.
    """

    fight_number = random.randrange(0,100)

    enemy_number = random.randrange(0,100)
    player_number = int(input("Hádej číslo v rozsahu 0 až 100. Pokud se trefíš blíž než nepřítel, vyhraješ!\n"))

    if player_number <= 0 or player_number >= 100:
        print(Fore.RED + "Zadáno neplatné číslo, vrácíme se zpět!")
        return

    enemy_difference = abs(fight_number - enemy_number)
    player_difference = abs(fight_number - player_number)

    print(f"Bojuješ s nepřítelem! Hádané číslo: {fight_number}")

    time.sleep(2)

    if player_difference < enemy_difference:
        print(Fore.GREEN + "Zvítězil jsi nad nepřítelem a získal jsi 100 peněz!")
        character['inventory'].append('poklad')
        character['coins'] += 100
    elif player_difference == enemy_difference:
        print(Fore.LIGHTBLACK_EX + "Boj byl nerozhodný, oba ustupujete.")
    else:
        print(Fore.RED + "Nepřítel byl příliš silný. Utrpěl jsi zranění.")
        character['health'] -= 30

        check_player_dead(character)

def check_player_dead(character):
    print("Byl jsi zabit!")
    print(Fore.BLUE + f"Počet peněz: {character['coins']}")
    raise PlayerDiedException("Hráč umřel, hra končí.")

def game_loop():
    print("Vítejte ve hře! Jak se jmenuješ?")

    character = create_character()

    # Vypíšeme informace o charakteru:
    print(Fore.BLUE + f"Jméno: {character['name']}, Životů: {character['health']}, Peněz: {character['coins']}, Počet itemů v inventáři: {len(character['inventory'])}")

    try:
        while True:
            action = get_player_choice(character)
            if action.lower() == 'quit':
                break
            process_action(action, character)
    except PlayerDiedException:
        return

class PlayerDiedException(Exception):
    """Výjimka pro situaci, kdy hráč umře ve hře."""
    pass