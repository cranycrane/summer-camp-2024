def caesar_sifra(text, posun):
    zasifrovany_text = ""
    for znak in text:
        if znak.isalpha():
            posunuty_znak = chr(((ord(znak.upper()) - 65 + posun) % 26) + 65)
            zasifrovany_text += posunuty_znak
        else:
            zasifrovany_text += znak
    return zasifrovany_text

# Testování šifrování
text = "skibidi gyatt wizz onwy in ohio duke dennis"
posun = 3
zasifrovany = caesar_sifra(text, posun)
print(f"Zasifrovany text: {zasifrovany}")


def caesar_desifruj(text, posun):
    desifrovany_text = ""
    for znak in text:
        if znak.isalpha():
            # Posunutí znaku zpět a obalení do intervalu A-Z
            posunuty_znak = chr((ord(znak.upper()) - ord('A') - posun) % 26 + ord('A'))
            desifrovany_text += posunuty_znak
        else:
            desifrovany_text += znak
    return desifrovany_text

# Testování dešifrování
zasifrovany_text = "vnlelgl"
posun = 3
#desifrovany = caesar_desifruj(zasifrovany_text, posun)
#print(f"Desifrovany text: {desifrovany}")
