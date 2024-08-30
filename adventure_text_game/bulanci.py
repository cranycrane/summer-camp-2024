import pygame
import random

# Inicializace Pygame
pygame.init()

# Nastavení velikosti okna
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animovaný hráč")

# Barvy
WHITE = (255, 255, 255)

# Parametry hráčů
player_size = (48, 48)
player1_pos = [WIDTH // 4, HEIGHT // 2]
player_speed = 5

# Načtení obrázku animace a rozřezání na jednotlivé snímky
sprite_sheet = pygame.image.load("sprite_sheet.png")
sprite_frames = []
for i in range(6):
    frame = sprite_sheet.subsurface(pygame.Rect(i * player_size[0], 0, player_size[0], player_size[1]))
    sprite_frames.append(frame)

# Počáteční snímek
current_frame = 0
frame_rate = 10  # Počet snímků za sekundu pro animaci
frame_counter = 0

# Hlavní smyčka hry
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pohyb hráče
    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_w]:
        player1_pos[1] -= player_speed
        moving = True
    if keys[pygame.K_s]:
        player1_pos[1] += player_speed
        moving = True
    if keys[pygame.K_a]:
        player1_pos[0] -= player_speed
        moving = True
    if keys[pygame.K_d]:
        player1_pos[0] += player_speed
        moving = True

    # Aktualizace snímků animace
    if moving:
        frame_counter += 1
        if frame_counter >= clock.get_fps() // frame_rate:
            current_frame = (current_frame + 1) % len(sprite_frames)
            frame_counter = 0
    else:
        current_frame = 0  # Pokud se hráč nepohybuje, nastavíme první snímek

    # Vyčištění obrazovky
    window.fill(WHITE)

    # Kreslení hráče (animovaný sprite)
    window.blit(sprite_frames[current_frame], player1_pos)

    # Aktualizace okna
    pygame.display.flip()

    # Nastavení FPS
    clock.tick(30)

# Ukončení Pygame
pygame.quit()
