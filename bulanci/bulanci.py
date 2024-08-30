import pygame
import random

# Inicializace Pygame
pygame.init()

# Nastavení velikosti okna
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bulánci - 2D Střílečka")

# Barvy
WHITE = (255, 255, 255)

# Parametry hráčů
player_size = (48, 48)
player1_pos = [WIDTH // 4, HEIGHT // 2]
player2_pos = [3 * WIDTH // 4 + 10, HEIGHT // 2]
player_speed = 5

# Načtení obrázků Bulánků
sprite_sheet_p1 = pygame.image.load("obrazky/p1.png")
sprite_frames_p1 = []
for i in range(6):
    frame = sprite_sheet_p1.subsurface(pygame.Rect(i * player_size[0], 0, player_size[0], player_size[1]))
    sprite_frames_p1.append(frame)

sprite_sheet_p2 = pygame.image.load("obrazky/p2.png")
sprite_frames_p2 = []
for i in range(6):
    frame = sprite_sheet_p2.subsurface(pygame.Rect(i * player_size[0], 0, player_size[0], player_size[1]))
    sprite_frames_p2.append(frame)

# Načtení obrázku střely
bullet_image = pygame.image.load("obrazky/bullet.png")
bullet_size = bullet_image.get_size()

# Načtení textur pro mapu (textury jsou 32x32 pixelů)
water_image = pygame.image.load("obrazky/water.png")
ground_image = pygame.image.load("obrazky/ground.png")

# Definice mapy pomocí řetězce
map_data = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W........W........W.....W",
    "W........W........W.....W",
    "W.......................W",
    "W.......................W",
    "W........W........W.....W",
    "W.......................W",
    "W.......................W",
    "W........W........W.....W",
    "W........W........W.....W",
    "W........W........W.....W",
    "W........W........W.....W",
    "W........W........W.....W",
    "W........W........W.....W",
    "W.......................W",
    "W.......................W",
    "W........W........W.....W",
    "W........W........W.....W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWW",
]

tile_size = 32  # Velikost dlaždice (32x32 pixelů)

# Střely
bullet_speed = 10
bullets = []

# Počáteční snímky a orientace pro oba hráče
current_frame_p1 = 0
current_frame_p2 = 0
frame_rate = 10  # Počet snímků za sekundu pro animaci
frame_counter_p1 = 0
frame_counter_p2 = 0
facing_right_p1 = True  # Počáteční směr pro hráče 1 (čelí doprava)
facing_right_p2 = True  # Počáteční směr pro hráče 2 (čelí doprava)

# Hlavní smyčka hry
running = True
clock = pygame.time.Clock()

# Funkce pro kontrolu kolizí s vodou
def check_collision_with_water(player_rect):
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile == "W":
                water_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                if player_rect.colliderect(water_rect):
                    return True
    return False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Vystřelení střely
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Hráč 1 střílí
                direction = 1 if facing_right_p1 else -1
                bullets.append({"pos": [player1_pos[0] + player_size[0] // 2, player1_pos[1] + player_size[1] // 2], "dir": direction, "shooter": "p1"})
            if event.key == pygame.K_RETURN:  # Hráč 2 střílí
                direction = 1 if facing_right_p2 else -1
                bullets.append({"pos": [player2_pos[0] + player_size[0] // 2, player2_pos[1] + player_size[1] // 2], "dir": direction, "shooter": "p2"})

    # Pohyb hráče 1
    keys = pygame.key.get_pressed()
    moving_p1 = False
    new_pos_p1 = player1_pos.copy()
    if keys[pygame.K_w]:
        new_pos_p1[1] -= player_speed
        moving_p1 = True
    if keys[pygame.K_s]:
        new_pos_p1[1] += player_speed
        moving_p1 = True
    if keys[pygame.K_a]:
        new_pos_p1[0] -= player_speed
        moving_p1 = True
        facing_right_p1 = False  # Hráč 1 se pohybuje doleva
    if keys[pygame.K_d]:
        new_pos_p1[0] += player_speed
        moving_p1 = True
        facing_right_p1 = True  # Hráč 1 se pohybuje doprava

    # Kontrola kolizí s vodou pro hráče 1
    player1_rect = pygame.Rect(new_pos_p1[0], new_pos_p1[1], player_size[0], player_size[1])
    if not check_collision_with_water(player1_rect):
        player1_pos = new_pos_p1

    # Pohyb hráče 2
    moving_p2 = False
    new_pos_p2 = player2_pos.copy()
    if keys[pygame.K_UP]:
        new_pos_p2[1] -= player_speed
        moving_p2 = True
    if keys[pygame.K_DOWN]:
        new_pos_p2[1] += player_speed
        moving_p2 = True
    if keys[pygame.K_LEFT]:
        new_pos_p2[0] -= player_speed
        moving_p2 = True
        facing_right_p2 = False  # Hráč 2 se pohybuje doleva
    if keys[pygame.K_RIGHT]:
        new_pos_p2[0] += player_speed
        moving_p2 = True
        facing_right_p2 = True  # Hráč 2 se pohybuje doprava

    # Kontrola kolizí s vodou pro hráče 2
    player2_rect = pygame.Rect(new_pos_p2[0], new_pos_p2[1], player_size[0], player_size[1])
    if not check_collision_with_water(player2_rect):
        player2_pos = new_pos_p2

    # Aktualizace snímků animace pro hráče 1
    if moving_p1:
        frame_counter_p1 += 1
        if frame_counter_p1 >= clock.get_fps() // frame_rate:
            current_frame_p1 = (current_frame_p1 + 1) % len(sprite_frames_p1)
            frame_counter_p1 = 0
    else:
        current_frame_p1 = 0  # Pokud se hráč nepohybuje, nastavíme první snímek

    # Aktualizace snímků animace pro hráče 2
    if moving_p2:
        frame_counter_p2 += 1
        if frame_counter_p2 >= clock.get_fps() // frame_rate:
            current_frame_p2 = (current_frame_p2 + 1) % len(sprite_frames_p2)
            frame_counter_p2 = 0
    else:
        current_frame_p2 = 0  # Pokud se hráč nepohybuje, nastavíme první snímek

    # Aktualizace střel
    for bullet in bullets[:]:
        bullet['pos'][0] += bullet['dir'] * bullet_speed

        # Vytvoření obdélníků pro kolize
        bullet_rect = pygame.Rect(bullet['pos'][0], bullet['pos'][1], bullet_size[0], bullet_size[1])
        player1_rect = pygame.Rect(player1_pos[0], player1_pos[1], player_size[0], player_size[1])
        player2_rect = pygame.Rect(player2_pos[0], player2_pos[1], player_size[0], player_size[1])

        # Kontrola kolize střely s hráčem 1, pokud ji nevystřelil on sám
        if bullet['shooter'] != "p1" and bullet_rect.colliderect(player1_rect):
            print("Hráč 1 byl zasažen!")
            bullets.remove(bullet)
            # Zde můžete přidat logiku pro zranění hráče, např. snížení životů

        # Kontrola kolize střely s hráčem 2, pokud ji nevystřelil on sám
        elif bullet['shooter'] != "p2" and bullet_rect.colliderect(player2_rect):
            print("Hráč 2 byl zasažen!")
            bullets.remove(bullet)
            # Zde můžete přidat logiku pro zranění hráče, např. snížení životů

    # Vyčištění obrazovky
    window.fill(WHITE)

    # Kreslení mapy
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile == "W":  # Zeď
                window.blit(water_image, (x * tile_size, y * tile_size))
            elif tile == ".":  # Podlaha
                window.blit(ground_image, (x * tile_size, y * tile_size))

    # Kreslení hráčů (Bulánků) s otočením podle směru pohybu
    player1_image = sprite_frames_p1[current_frame_p1]
    player2_image = sprite_frames_p2[current_frame_p2]

    if not facing_right_p1:
        player1_image = pygame.transform.flip(player1_image, True, False)  # Otočení vlevo
    if not facing_right_p2:
        player2_image = pygame.transform.flip(player2_image, True, False)  # Otočení vlevo

    window.blit(player1_image, player1_pos)
    window.blit(player2_image, player2_pos)

    # Kreslení střel
    for bullet in bullets:
        window.blit(bullet_image, bullet['pos'])

    # Aktualizace okna
    pygame.display.flip()

    # Nastavení FPS
    clock.tick(30)

# Ukončení Pygame
pygame.quit()
