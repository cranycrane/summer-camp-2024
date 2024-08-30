import random

"""
1. Ukol:
Vytvor promennou 'jmeno', kde ulozis vstup od uzivatele - jeho jmeno
Po zadani jmena ho pozdrav - vypis text
"""
jmeno = input("Zadej sve jmeno: ")
print(f"Ahoj {jmeno}")

"""
2. Ukol:
Vytvor promennou 'tajne_cislo' a vygeneruj nahodne cislo
s pomoci funkce 'random.randint(X,Y)', 
kde X je spodni hranice a Y vrchni hranice

Napriklad: 'random.randint(0,10)' vygeneruje nahodne cislo 
v rozsahu 0-10
"""
tajne_cislo = random.randint(0,100)



"""
UKOL:
Najdi a zjisti si, jak funguje 'while' v Pythonu
S pomoci 'while' vytvor cyklus, ktery bude ziskavat
tipy od uzivatele, dokud hadane cislo neuhodne

Vyuzij internet, ale treba i umelou inteligenci
"""


tip = input("Zadej svuj tip: ")


if tip > tajne_cislo:
    print("Tvuj tip byl vyssi")
elif tip < tajne_cislo:
    print("Tvuj tip byl mensi")
elif tip == tajne_cislo:
    print("Tvuj tip byl spravny!")



