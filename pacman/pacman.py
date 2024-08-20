import pygame
import sys

# Inicializace Pygame
pygame.init()

# Barvy
černá = (0, 0, 0)
modrá = (0, 0, 255)
žlutá = (255, 255, 0)
bílá = (255, 255, 255)

# Nastavení velikosti okna
velikost_bloku = 30
šířka_okna = 28 * velikost_bloku
výška_okna = 31 * velikost_bloku

okno = pygame.display.set_mode((šířka_okna, výška_okna))
pygame.display.set_caption("Jednoduchý Pac-Man")

# Statické bludiště
bludiště = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "######.##### ## #####.######",
    "######.##          ##.######",
    "######.## ######## ##.######",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#o..##................##..o#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################"
]

# Funkce pro vykreslení bludiště
def vykresli_bludiště(okno, bludiště):
    for řádek in range(len(bludiště)):
        for sloupec in range(len(bludiště[řádek])):
            znak = bludiště[řádek][sloupec]
            x = sloupec * velikost_bloku
            y = řádek * velikost_bloku
            if znak == "#":
                pygame.draw.rect(okno, modrá, (x, y, velikost_bloku, velikost_bloku))
            elif znak == ".":
                pygame.draw.circle(okno, bílá, (x + velikost_bloku // 2, y + velikost_bloku // 2), 5)
            elif znak == "o":
                pygame.draw.circle(okno, bílá, (x + velikost_bloku // 2, y + velikost_bloku // 2), 10)

# Hlavní třída pro Pac-Mana
class PacMan:
    def __init__(self):
        self.x = 1 * velikost_bloku
        self.y = 1 * velikost_bloku
        self.rychlost = velikost_bloku // 8
        self.směr_x = 0
        self.směr_y = 0
        self.score = 0
        self.tolerance_kolize = 2
        # Načtení obrázku Pac-Mana
        obrázek_pacman = pygame.image.load('obrazky/1.png')
        self.obrázek_pacman = pygame.transform.scale(obrázek_pacman, (velikost_bloku, velikost_bloku))


    def pohyb(self):
        next_x = self.x + self.směr_x
        next_y = self.y + self.směr_y

        # Ověření, zda všechny čtyři rohy Pac-Mana jsou mimo zeď
        if (bludiště[(next_y + self.tolerance_kolize) // velikost_bloku][(next_x + self.tolerance_kolize) // velikost_bloku] != "#" and
            bludiště[(next_y + velikost_bloku - 1 - self.tolerance_kolize) // velikost_bloku][(next_x + self.tolerance_kolize) // velikost_bloku] != "#" and
            bludiště[(next_y + self.tolerance_kolize) // velikost_bloku][(next_x + velikost_bloku - 1 - self.tolerance_kolize) // velikost_bloku] != "#" and
            bludiště[(next_y + velikost_bloku - 1 - self.tolerance_kolize) // velikost_bloku][(next_x + velikost_bloku - 1 - self.tolerance_kolize) // velikost_bloku] != "#"):
            self.x = next_x
            self.y = next_y


    def vykresli(self):
        okno.blit(self.obrázek_pacman, (self.x, self.y))

    def sbírej_bod(self):
        řádek = self.y // velikost_bloku
        sloupec = self.x // velikost_bloku
        if bludiště[řádek][sloupec] == ".":
            bludiště[řádek] = bludiště[řádek][:sloupec] + " " + bludiště[řádek][sloupec + 1:]
            self.score += 10
        elif bludiště[řádek][sloupec] == "o":
            bludiště[řádek] = bludiště[řádek][:sloupec] + " " + bludiště[řádek][sloupec + 1:]
            self.score += 50

def hra():
    pacman = PacMan()
    běží_hra = True
    hodiny = pygame.time.Clock()

    while běží_hra:
        for událost in pygame.event.get():
            if událost.type == pygame.QUIT:
                běží_hra = False
            elif událost.type == pygame.KEYDOWN:
                if událost.key == pygame.K_LEFT:
                    obrázek_pacman = pygame.image.load('obrazky/2.png')
                    pacman.obrázek_pacman = pygame.transform.scale(obrázek_pacman, (velikost_bloku, velikost_bloku))
                    pacman.směr_x = -pacman.rychlost
                    pacman.směr_y = 0
                elif událost.key == pygame.K_RIGHT:
                    obrázek_pacman = pygame.image.load('obrazky/1.png')
                    pacman.obrázek_pacman = pygame.transform.scale(obrázek_pacman, (velikost_bloku, velikost_bloku))
                    pacman.směr_x = pacman.rychlost
                    pacman.směr_y = 0
                elif událost.key == pygame.K_UP:
                    pacman.směr_x = 0
                    pacman.směr_y = -pacman.rychlost
                elif událost.key == pygame.K_DOWN:
                    pacman.směr_x = 0
                    pacman.směr_y = pacman.rychlost

        pacman.pohyb()
        pacman.sbírej_bod()

        okno.fill(černá)
        vykresli_bludiště(okno, bludiště)
        pacman.vykresli()

        # Zobrazení skóre
        font = pygame.font.SysFont(None, 35)
        score_text = font.render("Skóre: " + str(pacman.score), True, bílá)
        okno.blit(score_text, (10, 10))

        pygame.display.update()
        hodiny.tick(30)

    # Nabídka restartu nebo ukončení
    okno.fill(černá)
    font = pygame.font.SysFont(None, 55)
    text = font.render("Konec hry! Stiskni R pro restart nebo Q pro konec.", True, bílá)
    okno.blit(text, (50, výška_okna // 2))
    pygame.display.update()

    # Čeká na uživatelský vstup
    while True:
        for událost in pygame.event.get():
            if událost.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif událost.type == pygame.KEYDOWN:
                if událost.key == pygame.K_r:
                    hra()
                elif událost.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

hra()
