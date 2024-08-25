from colorama import Fore, Back, Style, init


def menic_barev(barva):
    if barva == 'red-fg':
        print(Fore.RED + 'Toto je červený text')
    elif barva == 'red-bg':
        print(Back.RED + 'Toto má červené pozadí')
    elif barva == 'green-fg':
        print(Fore.GREEN + 'Toto má zelené popředí')
    elif barva == 'green-bg':
        print(Back.GREEN + 'Toto má zelené pozadí')
    elif barva == 'blue-fg':
        print(Fore.BLUE + 'Toto má modré popředí')
    elif barva == 'blue-bg':
        print(Back.BLUE + 'Toto má modré pozadí')
    else:
        print("Neznámá barva.")

        
def získej_barvu():
    color_input = input("Jakou chceš barvu textu? ('red-fg', 'red-bg', 'green-fg', 'green-bg', 'blue-fg', 'blue-bg', 'quit'): ")
    print("Poznamka: 'fg' - foreground, popředí, 'bg' - background, záhlaví")
    return color_input


def main():
    init(autoreset=True)
    while True:
        barva = získej_barvu()
        if barva.lower() == 'quit':
            break
        menic_barev(barva)

if __name__ == "__main__":
    main()
