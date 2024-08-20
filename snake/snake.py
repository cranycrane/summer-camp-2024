import pygame
import random

# Inicializace Pygame
pygame.init()

# Nastavení velikosti okna
šířka_okna = 700
výška_okna = 700
okno = pygame.display.set_mode((šířka_okna, výška_okna))
pygame.display.set_caption("Had")

# Barvy
černá = (0, 0, 0)
zelená = (0, 255, 0)
bílá = (255, 255, 255)

# Nastavení hry
velikost_hada = 30  # Zvětšení velikosti hada a jablka
rychlost_hada = 7

# Načtení obrázků
obrázek_hlava = pygame.image.load('obrazky/hlava_hada.png')
obrázek_hlava = pygame.transform.scale(obrázek_hlava, (velikost_hada, velikost_hada))

obrázek_jablko = pygame.image.load('obrazky/jablko.png')
obrázek_jablko = pygame.transform.scale(obrázek_jablko, (velikost_hada, velikost_hada))

zpráva_font = pygame.font.SysFont("comicsansms", 35)

def skore(score):
    value = zpráva_font.render("Skóre: " + str(score), True, bílá)
    okno.blit(value, [0, 0])

def zpráva(msg, color):
    mesg = zpráva_font.render(msg, True, color)
    okno.blit(mesg, [šířka_okna / 6, výška_okna / 3])

# Hlavní funkce hry
def hra():
    # Startovní pozice hada
    x = šířka_okna // 2
    y = výška_okna // 2
    x_ruch = 0
    y_ruch = 0

    # Had jako seznam segmentů
    tělo_hada = []
    délka_hada = 1

    # Funkce pro generování jídla zarovnaného podle velikosti hada
    def generuj_jidlo():
        return (
            round(random.randrange(0, šířka_okna - velikost_hada) / velikost_hada) * velikost_hada,
            round(random.randrange(0, výška_okna - velikost_hada) / velikost_hada) * velikost_hada
        )

    # Generování první pozice jídla
    jídlo_x, jídlo_y = generuj_jidlo()

    běží_hra = True

    while běží_hra:
        # Zpracování událostí (ovládání šipkami)
        for událost in pygame.event.get():
            if událost.type == pygame.QUIT:
                běží_hra = False
            if událost.type == pygame.KEYDOWN:
                if událost.key == pygame.K_LEFT:
                    x_ruch = -velikost_hada
                    y_ruch = 0
                elif událost.key == pygame.K_RIGHT:
                    x_ruch = velikost_hada
                    y_ruch = 0
                elif událost.key == pygame.K_UP:
                    x_ruch = 0
                    y_ruch = -velikost_hada
                elif událost.key == pygame.K_DOWN:
                    x_ruch = 0
                    y_ruch = velikost_hada

        # Pohyb hada
        x += x_ruch
        y += y_ruch

        # Kontrola kolize s okraji
        if x < 0 or x >= šířka_okna or y < 0 or y >= výška_okna:
            běží_hra = False

        # Aktualizace těla hada
        hlava = [x, y]
        tělo_hada.append(hlava)
        if len(tělo_hada) > délka_hada:
            del tělo_hada[0]

        # Kontrola, zda had narazil do sebe
        for segment in tělo_hada[:-1]:
            if segment == hlava:
                běží_hra = False

        # Detekce kolize hada s jablkem
        if pygame.Rect(x, y, velikost_hada, velikost_hada).colliderect(pygame.Rect(jídlo_x, jídlo_y, velikost_hada, velikost_hada)):
            jídlo_x, jídlo_y = generuj_jidlo()
            délka_hada += 1

        # Vykreslení hry
        okno.fill(černá)

        # Vykreslení obrázku jablka
        okno.blit(obrázek_jablko, (jídlo_x, jídlo_y))

        # Vykreslení obrázku hlavy hada
        okno.blit(obrázek_hlava, (x, y))

        skore(délka_hada - 1)

        # Vykreslení těla hada
        for segment in tělo_hada[:-1]:  # Hlava se už vykreslila, takže zbytek těla
            pygame.draw.rect(okno, zelená, [segment[0], segment[1], velikost_hada, velikost_hada])

        pygame.display.update()

        # Nastavení rychlosti hry
        pygame.time.Clock().tick(rychlost_hada)

    # Zobrazí zprávu po ukončení hry
    okno.fill(černá)
    zpráva("Prohrál jsi! Stiskni R pro znovu, Q pro konec.", bílá)
    pygame.display.update()

    # Čeká na uživatelský vstup (R pro restart, Q pro ukončení)
    while True:
        for událost in pygame.event.get():
            if událost.type == pygame.KEYDOWN:
                if událost.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if událost.key == pygame.K_r:
                    hra()

# Spuštění hry
hra()
