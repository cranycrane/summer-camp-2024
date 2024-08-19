from colorama import Fore, Back, Style
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
    print(f"Ahoj, {character_name}, tvé dobrodružství začíná...")
    return character_name

def get_player_choice():
    return input("Co chceš dělat? (např. 'prozkoumat', 'mluvit', 'bojovat', 'quit'): ")

def process_action(action):
    if action == 'prozkoumat':
        explore()
    elif action == 'obchodovat':
        trade()
    elif action == 'mluvit':
        talk()
    elif action == 'bojovat':
        fight()
    else:
        print("Neznámá akce.")

def explore():
    print("Prozkoumáváš oblast.")

def trade(character):
    """
    Umožňuje hráči nakupovat předměty.

    Parameters:
    character (dict): Slovník obsahující informace o postavě, včetně mincí a inventáře.
    """
    items_for_sale = {
        1: {'name': '+1 Život', 'price': 50},
        2: {'name': '+1 Síla', 'price': 75},
        3: {'name': 'Kouzelný lektvar', 'price': 100}
    }
    
    # Zobrazí dostupné předměty a jejich ceny
    print("Dostupné předměty k nákupu:")
    for key, item in items_for_sale.items():
        print(f"({key}) {item['name']} - Cena: {item['price']} mincí")
    
    # Získá uživatelský vstup
    try:
        product_number = int(input("Co chceš nakoupit? (Vyber číslo): "))
        product = items_for_sale.get(product_number)
        if product is None:
            print("Neplatný výběr.")
            return

        # Kontrola, zda má hráč dost mincí
        if character['coins'] < product['price']:
            print("Nemáš dost mincí na koupi tohoto předmětu.")
            # Vrátí se zpět do hlavní smyčky
            return

        # Odečtení peněz charaktera
        character['coins'] -= product['price']
        # Přidání itemu do inventáře
        character['inventory'].append(product['name'])

        print(f"Zakoupil jsi {product['name']}. Zbývající mince: {character['coins']}.")

    except ValueError:
        print("Prosím zadej platné číslo.")

    pass

def talk():
    print("Mluvíš s postavou.")

def fight():
    print("Bojuješ s nepřítelem.")

def outro():
    print("Konec hry. Díky za hraní!")


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
        process_action(action)