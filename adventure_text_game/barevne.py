from colorama import Fore, Back, Style, init


def menic_barev(color):
    if color == 'red-fg':
        print(Fore.RED + 'Toto je červený text')
    elif color == 'red-bg':
        print(Back.RED + 'Toto má červené pozadí')
    elif color == 'green-fg':
        print(Fore.GREEN + 'Toto má zelené popředí')
    elif color == 'green-bg':
        print(Back.GREEN + 'Toto má zelené pozadí')
    elif color == 'blue-fg':
        print(Fore.BLUE + 'Toto má modré popředí')
    elif color == 'blue-bg':
        print(Back.BLUE + 'Toto má modré pozadí')
    else:
        print("Neznámá barva.")

        
def get_player_color():
    color_input = input("Jakou chceš barvu textu? ('red-fg', 'red-bg', 'green-fg', 'green-bg', 'blue-fg', 'blue-bg', 'quit'): ")
    print("Poznamka: 'fg' - foreground, popředí, 'bg' - background, záhlaví")
    return color_input


def main():
    init(autoreset=True)
    while True:
        color = get_player_color()
        if color.lower() == 'quit':
            break
        menic_barev(color)

if __name__ == "__main__":
    main()
