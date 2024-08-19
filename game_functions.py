from colorama import Fore, Back, Style
import random
"""
Knihovny: unittest, coloroma


"""

def create_character():
    # Vytvoření proměnných pro jméno postavy, zdraví, sílu a inventář
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

def get_character_name():
    character_name = input("Zadej jméno: ")
    
    if len(character_name) == 0:
        print(Fore.RED + "Chyba: Název charakteru nesmí být prázdný")
        character_name = 'Hrdina'

    print(f"Ahoj, {character_name}, tvé dobrodružství začíná...")
    return character_name

def get_player_choice():
    return input("Co chceš dělat? (např. 'prozkoumat', 'mluvit', 'bojovat', 'obchodovat', 'quit'): ")

def process_action(action, character):
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
    discoveries = ["starý meč", "zlatá mince", "magický amulet", "nic"]

    found_item = random.choice(discoveries)
    
    if found_item != "nic":
        character['inventory'].append(found_item)
        print(f"Našel jsi {found_item}!")
    else:
        print("Prozkoumal jsi oblast, ale nenašel jsi nic zajímavého.")

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
    print("Dostupné předměty k nákupu:")
    for index, item in enumerate(items_for_sale):
        print(f"({index + 1}) {item['name']} - Cena: {item['price']} mincí")
    
    # Získání uživatelského vstupu
    product_index = int(input("Co chceš nakoupit? (Vyber číslo): ")) - 1
    if product_index < 0 or product_index >= len(items_for_sale):
        print("Neplatný výběr.")
        return

    product = items_for_sale[product_index]

    # Kontrola, zda má hráč dost mincí
    if character['coins'] < product['price']:
        print("Nemáš dost mincí na koupi tohoto předmětu.")
        return

    # Provedení nákupu
    character['coins'] -= product['price']
    character['inventory'].append(product['name'])
    print(f"Zakoupil jsi {product['name']}. Zbývající mince: {character['coins']}.")


def talk(character):
    print("Mluvíš s postavou.")

def fight(character):
    print("Bojuješ.")

def game_loop():
    print("Vítejte ve hře! Jak se jmenuješ?")

    character = create_character()

    print(f"Ahoj, {character["name"]}, tvé dobrodružství začíná...")
    # Vypíšeme informace o charakteru:
    print(Fore.BLUE + f"Jméno: {character["name"]}, Životů: {character["health"]}, Peněz: {character["coins"]}, Počet itemů v inventáři: {len(character["inventory"])}")

    while True:
        action = get_player_choice()
        if action.lower() == 'quit':
            break
        process_action(action, character)