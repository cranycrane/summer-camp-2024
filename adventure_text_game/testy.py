from colorama import Fore, Back, Style, init


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

    ############## Doplň kód ###############

    return jméno_charaktera

    ########################################

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