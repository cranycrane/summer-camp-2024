from colorama import Fore, Back, Style, init
import random
import time
import pygame



"""
    Úkol - proměnné 1
    Zadání:
    1. Oprav kód ve vyznačené oblasti
    2. Pozdrav hráče pomocí funkce 'print', v barevne.py najdeš, jak se tato funkce používá k výpisu proměnných
    3. Doplň chybějící kód ve vyznačené oblasti (Nápověda: všimni si, že funkce má vrátit 'str' - řetězec)
"""
def získej_jméno_charaktera() -> str:
    """
    Zeptá se hráče, jaké chce mít jméno charakteru a pozdraví ho

    Returns:
        str: Jméno charakteru zadané uživatelem
    """

    ########### Oprav tento kód ############
    jméno_charaktera = input("Zadej jméno: ")
    ########################################


    if len(jméno_charaktera) == 0:
        print(Fore.RED + "Chyba: Název charakteru nesmí být prázdný")
        jméno_charaktera = 'Hrdina'

    print(f"Ahoj, {jméno_charaktera}, tvé dobrodružství začíná...")

    ############## Doplň kód ###############
    return jméno_charaktera
    ########################################


"""
    ÚKOL - proměnné - 2
    Zadání:
    1.Vytvoř proměnné pro charakter: 
    - životy s hodnotou 100
    - peníze s hodnotou 0
    - inventář jako prázdní pole

    2. V části 'return' u položky 'jméno' zavolej funkci 'získej jméno_charaktera'
    3. V části 'return' doplň proměnné 'životy', 'peníze' a 'inventář', které sis vytvořil
"""
def vytvoř_charakter():

    ############## Doplň kód ###############
    # Vytvoření proměnných pro jméno postavy, zdraví, peníze a inventář

    životy = 100  # Číslo
    peníze = 0  # Číslo
    inventář = []  # Pole/Seznam/List

    # Vrátíme informace o charakteru
    return {
        "jméno": získej_jméno_charaktera(),
        "životy": životy,
        "peníze": peníze,
        "inventář": inventář
    }
    ########################################


"""
    ÚKOL - proměnné - 3
    Zadání:
    1. Uprav funkci tak, aby pomocí funkce 'print' vypsala informace o charakteru v tomto formátu:¨
        Životy: počet_životů
        Peníze: počet_peněz
        Inventář: 'jednotlivé předměty z inventáře'
"""
def zobraz_informace_charakteru(charakter):
    print("-----------------------------------------------------------------------")
    ############## Doplň kód ###############
    print(Fore.RED + f"Životy: {charakter['životy']}" )
    print(Fore.BLUE + f"Peníze: {charakter['peníze']}" )
    ########################################
    print(Fore.LIGHTMAGENTA_EX + "Inventář:")
    for předmět in charakter['inventář']:
        print(předmět)
    print("-----------------------------------------------------------------------")


"""
    ÚKOL - funkce 1
    Zadání:
    1. Doplň funkci tak, aby získala vstup uživatele s akcí, co chce dělat 
    (funkce 'input', podívej se na funkci 'získej_jméno_charaktera'),
    nezapomeň uživateli zobrazit, jaké akce jsou k dispozici - 'prozkoumat', 'mluvit', 'bojovat', 'obchodovat', 'odejít'
"""
def získej_akci_hráče() -> str:
    """
    Zeptá se hráče, jakou chce provést akci a vypíše základní informace o charakteru
    """
    ############## Doplň kód ###############
    return input("Co chceš dělat? (např. 'prozkoumat', 'mluvit', 'bojovat', 'obchodovat', 'odejit'): ")
    ########################################


"""
    ÚKOL - funkce a podmínky
    Zadání:
    1. Doplň funkci tak, aby se zadanou akcí od uživatele zavolala odpovídající funkci
    Nápověda: Podívej se do souboru 'barevne.py'
"""
def zpracuj_akci(akce, charakter):
    """
    Zavolá odpovídající funkci dle typu akce

    Parameters:
    akce (str): Řetězec obsahující název akce - získaný ve funkci 'získej_akci_hráče'
    charakter (dict): Slovník obsahující informace o postavě, včetně mincí a inventáře.
    """

    ############## Doplň kód ###############
    if akce == 'prozkoumat':
        prozkoumat(charakter)
    elif akce == 'obchodovat':
        obchodovat(charakter)
    elif akce == 'mluvit':
        mluvit(charakter)
    elif akce == 'bojovat':
        bojovat(charakter)
    else:
        print("Neznámá akce.")
    ########################################


"""
    ÚKOL - proměnné - 3
    Zadání:
    1. Přidej do proměnné 'objevy' další předměty - cokoliv tě napadne
    2. Uprav podmínku tak, aby pokud bylo nalezeno 'nic', aby se objevil odpovídající výstup
"""
def prozkoumat(charakter):
    print("Prozkoumáváš okolí...")

    time.sleep(2)

    objevy = ["starý meč", "zlatá mince", "magický amulet", "nic"]

    nalezený_item = random.choice(objevy)
    
    ############## Doplň kód do podmínky ###############
    if nalezený_item != "nic":
        charakter['inventář'].append(nalezený_item)
        print(Fore.GREEN + f"Našel jsi {nalezený_item}!")
        hrej_zvuk("zvuky/coin.mp3")
    else:
        print(Fore.LIGHTBLACK_EX + "Prozkoumal jsi oblast, ale nenašel jsi nic zajímavého.")
    ####################################################


"""
    ÚKOL - funkce a proměnné
    Zadání:
    1. Přidej další předmět na prodej
    2. Přidej podmínku, kontrolu, zda má hráč dost peněz pro zakoupení předmětu ve vyznačené oblasti
    Pokud nemá dost peněz - vypiš odpovídající zprávu a vrať se z funkce (return), jinak pokračuj
    3. Odečti charakteru peníze a vypiš název zakoupeného předmětu a kolik peněz charakteru zbývá
"""
def obchodovat(charakter):
    """
    Umožňuje hráči nakupovat předměty.

    Parameters:
    charakter (dict): Slovník obsahující informace o postavě, včetně mincí a inventáře.
    """
    předměty_na_prodej = [
        {'jméno': 'Život', 'cena': 50},
        {'jméno': 'Síla', 'cena': 75},
        {'jméno': 'Kouzelný lektvar', 'cena': 100}
    ]
    
    # Zobrazení dostupných předmětů a jejich cen
    print(Fore.LIGHTMAGENTA_EX +  "Dostupné předměty k nákupu:")
    for index, předmět in enumerate(předměty_na_prodej):
        print(f"({index + 1}) {předmět['jméno']} - Cena: {předmět['cena']} mincí")
    
    # Získání uživatelského vstupu
    index_produktu = int(input("Co chceš nakoupit? (Vyber číslo): ")) - 1


    print(f"index_produktu: {index_produktu}")
    if index_produktu < 0 or index_produktu >= len(předměty_na_prodej):
        print(Fore.RED +  "Neplatný výběr.")
        return

    předmět = předměty_na_prodej[index_produktu]

    # Kontrola, zda má hráč dost mincí
    ############## Doplň kód ###############
    if charakter['peníze'] < předmět['cena']:
        print(Fore.RED + "Nemáš dost mincí na koupi tohoto předmětu.")
        return
    ########################################

    # Provedení nákupu, všimni si, jak se přistupuje k informacím předmětu
    ############## Doplň kód ###############
    charakter['peníze'] -= předmět['cena']
    charakter['inventář'].append(předmět['jméno'])
    print(f"Zakoupil jsi {předmět['jméno']}. Zbývající mince: {charakter['peníze']}.")
    ########################################


def mluvit(charakter):
    print(Fore.BLUE + "Mluvíš s postavou.")
    hrej_zvuk('./zvuky/intro.mp3')


"""
    ÚKOL - podmínky
    Zadání:
    1. Přidej podmínku, pokud je hráč mrtvý, pokud ano, vypiš odpovídající výstup a přidej na konec podmínky tento řádek kódu:
    raise PlayerDiedException("Hráč umřel, hra končí.")
"""
def zkontroluj_žije_hráč(charakter):
    ############## Doplň kód ###############
    if charakter["životy"] <= 0:
        print("Byl jsi zabit!")
        print(Fore.BLUE + f"Počet peněz: {charakter['peníze']}")
        raise PlayerDiedException("Hráč umřel, hra končí.")
    ########################################


"""
    ÚKOL - funkce, proměnné a podmínky
    Zadání:
    1. Přidej podmínky pro 'číslo_hráč', zda zadal hodnotu ve správném rozsahu 0 až 100, 
    pokud ne, vrať se z funkce
    2. Přidej zvuk pro boj pomocí funkce 'hrej_zvuk' - podívej se do složky zvuky
    3. Oprav podmínku pro rozdíl hráče a nepřítele
    4. Doplň kód:
    Pokud hráč vyhrál, přidej charakteru 100 peněz
    Pokud prohrál, uber mu 30 životů a zavolej funkci 'zkontroluj_žije_hráč'
"""
def bojovat(charakter):
    """
    Boj s příšerou na základě hádání čísla od 0 po 100.
    Příšera hadá taky. Ten kdo uhodne blíž, vyhrává.

    Parameters:
    charakter (dict): Slovník obsahující informace o postavě, včetně mincí a inventáře.
    """

    bojovací_číslo = random.randrange(0,100)

    číslo_nepřítel = random.randrange(0,100)
    číslo_hráč = int(input("Hádej číslo v rozsahu 0 až 100. Pokud se trefíš blíž než nepřítel, vyhraješ!\n"))

    if číslo_hráč < 0 or číslo_hráč > 100:
        print(Fore.RED + "Zadáno neplatné číslo, vrácíme se zpět!")
        return

    rozdíl_nepřítele = abs(bojovací_číslo - číslo_nepřítel)
    rozdíl_hráče = abs(bojovací_číslo - číslo_hráč)

    print(f"Bojuješ s nepřítelem! Hádané číslo: {bojovací_číslo}")

    ############## Doplň zvuk pro boj ###############

    hrej_zvuk("zvuky/fight.mp3")

    #################################################


    time.sleep(2)

    ########### Oprav podmínky a doplň kód dle bodu 4 ############
    if rozdíl_hráče < rozdíl_nepřítele:
        print(Fore.GREEN + "Zvítězil jsi nad nepřítelem a získal jsi 100 peněz!")
        charakter['inventář'].append('poklad')
        hrej_zvuk("zvuky/coin.mp3")
        charakter['peníze'] += 100
    elif rozdíl_hráče == rozdíl_nepřítele:
        print(Fore.LIGHTBLACK_EX + "Boj byl nerozhodný, oba ustupujete.")
    else:
        print(Fore.RED + "Nepřítel byl příliš silný. Utrpěl jsi zranění.")
        hrej_zvuk("zvuky/dead.mp3")
        charakter['životy'] -= 30

        zkontroluj_žije_hráč(charakter)

    ##############################################################


def smyčka_hry():
    print("Vítejte ve hře! Jak se jmenuješ?")

    charakter = vytvoř_charakter()

    try:
        while True:
            zobraz_informace_charakteru(charakter)
            akce = získej_akci_hráče()
            if akce.lower() == 'odejit':
                break
            zpracuj_akci(akce, charakter)
    except PlayerDiedException:
        return
    
def hrej_zvuk(file_path, hlasitost=1.0):
    pygame.init()
    pygame.mixer.init()
    zvuk = pygame.mixer.Sound(file_path)
    zvuk.set_volume(hlasitost)
    zvuk.play()

def main():
    hrej_zvuk("./zvuky/hudba.mp3", 0.4)
    init(autoreset=True)
    smyčka_hry()

if __name__ == "__main__":
    main()        

class PlayerDiedException(Exception):
    """Výjimka pro situaci, kdy hráč umře ve hře."""
    pass