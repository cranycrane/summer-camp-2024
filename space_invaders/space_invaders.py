import pygame
import random
import math

# Inicializace Pygame
pygame.init()

# Nastavení velikosti okna
šířka_okna = 800
výška_okna = 600
okno = pygame.display.set_mode((šířka_okna, výška_okna))

# Titulek a ikona
pygame.display.set_caption("Space Invaders")

# Hráč
hráč = pygame.image.load("obrazky/hrac.png")
hráč_x = 370
hráč_y = 480
hráč_rychlost = 5
životy = 3

# Nepřítel
nepřítel = []
nepřítel_x = []
nepřítel_y = []
nepřítel_rychlost_x = []
nepřítel_rychlost_y = []
nepřítel_střelba_interval = []
nepřítel_poslední_střelba = []
počet_nepřátel = 6

for i in range(počet_nepřátel):
    nepřítel.append(pygame.image.load("obrazky/bomber.png"))
    nepřítel_x.append(random.randint(0, 736))
    nepřítel_y.append(random.randint(50, 150))
    nepřítel_rychlost_x.append(1.5)
    nepřítel_rychlost_y.append(30)
    nepřítel_střelba_interval.append(random.randint(1000, 3000))  # Interval střelby v milisekundách
    nepřítel_poslední_střelba.append(pygame.time.get_ticks())  # Poslední čas střelby

# Projektily nepřátel
nepřátelské_projektily = []

def vystřel_nepřítel(x, y):
    nepřátelské_projektily.append([x + 16, y + 40])  # Přidáme projektil s pozicí blízko nepřítele

# Projektil hráče
projektil = pygame.image.load("obrazky/projektil.png")
projektil_x = 0
projektil_y = 480
projektil_rychlost = 20
projektil_střelba = False

# Výbuch
výbuch_obrázek = pygame.image.load("obrazky/exploze.png")
výbuch_obrázek = pygame.transform.scale(výbuch_obrázek, (64, 64))
výbuch_snímků = 0

# Skóre
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10

# Načtení obrázku srdce
srdce_obrázek = pygame.image.load("obrazky/zivot.png")
# Nastavíme velikost srdce
srdce_obrázek = pygame.transform.scale(srdce_obrázek, (32, 32))  


"""
    Úkol 1 - Výpis skóre:
    Zadání:
    1. Implementujte změnu barvy textu skóre na základě výše skóre.
    2. Barva se mění na zelenou, pokud je skóre vyšší než 5, jinak na bílou.
"""

def zobraz_score(x, y):
    if score >= 15:
        skóre = font.render("Skóre : " + str(score), True, (0, 255, 0))  # Zelená
    else:
        skóre = font.render("Skóre : " + str(score), True, (255, 255, 255))  # Bílá
    okno.blit(skóre, (x, y))


"""
    Úkol 2 - Dynamická změna barvy pozadí životů:
    Zadání:
    1. Napište smyčku, která bude v herní funkci 'zobraz_životy' zobrazovat životy hráče.
    2. Každé srdce reprezentuje jeden život a je vykresleno vedle sebe s daným rozestupem.
    3. Upravte barvu pozadí za srdci:
       - Pokud zbývá jeden život, nastavte pozadí na červenou.
       - Pokud zbývají dva životy, nastavte pozadí na oranžovou.
       - Pro více než dva životy použijte standardní barvu.
    4. Implementaci proveďte tak, aby se pozadí měnilo před vykreslením srdcí.
"""

def zobraz_životy(x, y):
    # Nastavení barvy pozadí podle počtu životů
    if životy == 1:
        pozadí_barva = (255, 0, 0)  # Červená barva pro 1 život
    elif životy == 2:
        pozadí_barva = (255, 165, 0)  # Oranžová barva pro 2 životy
    else:
        pozadí_barva = (255, 255, 255)  # Standardní bílá barva pro 3 a více životů

    # Vykreslení pozadí za srdci
    pozadí_rect = pygame.Rect(x, y, životy * 40, 32)
    okno.fill(pozadí_barva, pozadí_rect)

    # Vykreslení srdcí
    for i in range(životy):
        okno.blit(srdce_obrázek, (x + i * 40, y))

def uber_život():
    global životy
    životy -= 1
    if životy <= 0:
        konec_hry()

def konec_hry():
    okno.fill((0, 0, 0))
    
    font_konec = pygame.font.Font("freesansbold.ttf", 64)
    text_konec = font_konec.render("Konec hry", True, (255, 255, 255))
    text_skore = font.render(f"Skóre: {score}", True, (255, 255, 255))
    
    okno.blit(text_konec, (šířka_okna // 2 - text_konec.get_width() // 2, výška_okna // 3))
    okno.blit(text_skore, (šířka_okna // 2 - text_skore.get_width() // 2, výška_okna // 2))
    
    pygame.display.update()
    
    pygame.time.delay(3000)

    pygame.quit()
    quit()

def vykresli_hráče(x, y):
    okno.blit(hráč, (x, y))

def vykresli_nepřítele(x, y, i):
    okno.blit(nepřítel[i], (x, y))

"""
    Úkol 3 - Pohyb projektilu:
    Zadání:
    1. Upravte směr a rychlost projektilů hráče na základě aktuální pozice hráče.
    2. Projektil by měl směřovat nahoru.

    Rada:
      Jednu souřadnici musíš zvýšit o 16 a druhou o 10
"""

def vystřel_projektil(x, y):
    global projektil_střelba
    projektil_střelba = True
    projektil_x = x + 16    
    projektil_y = y+10
    okno.blit(projektil, (projektil_x, projektil_y))


"""
    Úkol 4 - Detekce kolize pomocí matematického vzorce:
    Zadání:
    1. Implementujte funkci 'je_kolize', která zjistí, zda došlo ke kolizi mezi nepřítelem a projektilu.
    2. Použijte k tomu matematický vzorec pro výpočet vzdálenosti mezi dvěma body na obrazovce:
       √((x2 - x1)^2 + (y2 - y1)^2)

    Rada:
    - Použijte funkci 'math.sqrt' pro výpočet druhé odmocniny a 'math.pow' pro umocnění na druhou.
    - Vzorec můžete zapsat přímo do proměnné 'vzdálenost'.
"""   

def je_kolize(nepřítel_x, nepřítel_y, projektil_x, projektil_y):
    vzdálenost = math.sqrt(math.pow(nepřítel_x - projektil_x, 2) + math.pow(nepřítel_y - projektil_y, 2))
    return vzdálenost < 27

def zobraz_výbuch(x, y):
    hrej_zvuk("zvuky/exploze.mp3")
    global výbuch_snímků, výbuch_pozice
    výbuch_pozice = (x, y)
    výbuch_snímků = 30

def hrej_zvuk(file_path, hlasitost=1.0):
    sound = pygame.mixer.Sound(file_path)
    sound.set_volume(hlasitost)
    sound.play()

# Hudba ve hře
hrej_zvuk("zvuky/hudba.ogg", 0.5)

# Nastavení fontu pro text pauzy
font = pygame.font.Font(None, 48)  # Vybere defaultní font ve velikosti 48
pause_text = font.render("Pauza - stiskněte 'P' pro pokračování", True, (255, 255, 255))
pause_text_rect = pause_text.get_rect(center=(šířka_okna / 2, výška_okna / 2))

# Herní smyčka
clock = pygame.time.Clock()
běží_hra = True
pauza = False
last_enemy_add_score = 0


"""
    Úkol 5 - Pauza ve hře:
    Zadání:
    1. Implementujte funkci pauzy, která se aktivuje a deaktivuje stiskem klávesy 'P'.
    2. Během pauzy se veškerý pohyb a akce nepřátel zastaví.
    3. Na obrazovce se objeví text "Pauza - stiskněte 'P' pro pokračování".
"""


"""
    Úkol 6 - Změna barvy pozadí:
    Zadání:
    1. Změňte barvu pozadí hry, když hráč dosáhne skóre 10 nebo více.
    2. Pokud je skóre 10 nebo vyšší, nastavte pozadí na šedou barvu.
    3. Tuto změnu proveďte v herní smyčce na začátku každé iterace.
"""


"""
    Úkol 7 - Dynamická změna rychlosti hráče:
    Zadání:
    1. Upravte rychlost hráče tak, aby se měnila v závislosti na skóre.
    2. Pokud je skóre nižší než 10, hráč se pohybuje standardní rychlostí.
    3. Pokud je skóre 10 nebo vyšší, zvýší se rychlost hráče na dvojnásobek standardní rychlosti.
    4. Implementaci proveďte uvnitř hlavní herní smyčky.
"""
while běží_hra:
    if score >= 10:
        okno.fill((128, 128, 128))  # Šedá barva
    else:
        okno.fill((0, 0, 0))  # Standardní černá barva

    for událost in pygame.event.get():
        if událost.type == pygame.QUIT:
            běží_hra = False
        elif událost.type == pygame.KEYDOWN:
            if událost.key == pygame.K_p:
                pauza = not pauza

    if score >= 5:
        hráč_rychlost = 10  # Zvýšení rychlosti hráče na dvojnásobek
    else:
        hráč_rychlost = 5  # Standardní rychlost hráče
    
    klávesy = pygame.key.get_pressed()
    if klávesy[pygame.K_LEFT] and hráč_x > 0:
        hráč_x -= hráč_rychlost
    if klávesy[pygame.K_RIGHT] and hráč_x < šířka_okna - 64:
        hráč_x += hráč_rychlost
    if klávesy[pygame.K_UP] and hráč_y > 0:
        hráč_y -= hráč_rychlost
    if klávesy[pygame.K_DOWN] and hráč_y < výška_okna - 64:
        hráč_y += hráč_rychlost

    if klávesy[pygame.K_SPACE]:
        if not projektil_střelba:
            projektil_x = hráč_x
            projektil_y = hráč_y
            vystřel_projektil(projektil_x, projektil_y)

    # Pohyb nepřátel a jejich střelba
    if not pauza:
        for i in range(počet_nepřátel):
            nepřítel_x[i] += nepřítel_rychlost_x[i]
            if nepřítel_x[i] <= 0:
                nepřítel_rychlost_x[i] = 1.5
                nepřítel_y[i] += nepřítel_rychlost_y[i]
            elif nepřítel_x[i] >= 736:
                nepřítel_rychlost_x[i] = -1.5
                nepřítel_y[i] += nepřítel_rychlost_y[i]

            # Nepřátelská střelba
            if pygame.time.get_ticks() - nepřítel_poslední_střelba[i] > nepřítel_střelba_interval[i]:
                vystřel_nepřítel(nepřítel_x[i], nepřítel_y[i])
                nepřítel_poslední_střelba[i] = pygame.time.get_ticks()

            # Kolize
            kolize = je_kolize(nepřítel_x[i], nepřítel_y[i], projektil_x, projektil_y)
            if kolize:
                zobraz_výbuch(nepřítel_x[i], nepřítel_y[i])
                projektil_y = 480
                projektil_střelba = False
                score += 1
                nepřítel_x[i] = random.randint(0, 736)
                nepřítel_y[i] = random.randint(50, 150)

            vykresli_nepřítele(nepřítel_x[i], nepřítel_y[i], i)

        # Pohyb projektilu hráče
        if projektil_střelba:
            vystřel_projektil(projektil_x, projektil_y)
            projektil_y -= projektil_rychlost
        if projektil_y <= 0:
            projektil_y = 480
            projektil_střelba = False

        # Pohyb nepřátelských projektilů
        for nepřítel_projektil in nepřátelské_projektily:
            nepřítel_projektil[1] += 5  # Rychlost projektilu směrem dolů
            okno.blit(pygame.image.load("obrazky/projektil.png"), (nepřítel_projektil[0], nepřítel_projektil[1]))

            # Detekce kolize s hráčem
            if je_kolize(nepřítel_projektil[0], nepřítel_projektil[1], hráč_x, hráč_y):
                zobraz_výbuch(hráč_x, hráč_y)
                uber_život()
                nepřátelské_projektily.remove(nepřítel_projektil)

        if výbuch_snímků > 0:
            okno.blit(výbuch_obrázek, výbuch_pozice)
            výbuch_snímků -= 1


        # Vykreslení hráče a skóre
        vykresli_hráče(hráč_x, hráč_y)
        zobraz_score(text_x, text_y)
        zobraz_životy(text_x, text_y + 40)
    else:
        okno.blit(pause_text, pause_text_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
