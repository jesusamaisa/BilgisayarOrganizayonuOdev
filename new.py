import pygame
import time
import random

# Pygame başlat
pygame.init()

# Ekran boyutu
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MÖTHÖŞ OYUN")

# Renkler
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GREEN = (0, 200, 0)
GRAY = (100, 100, 100)
YELLOW = (200, 200, 0)

# Bellek seviyeleri (y koordinatları)
levels = {
    "Register": 50,
    "Cache": 150,
    "RAM": 250,
    "Disk": 350
}

# Veri blokları
class DataBlock:
    def __init__(self, x, y, target_level):
        self.x = x
        self.y = y
        self.target_y = levels[target_level]
        self.color = YELLOW
        self.speed = 2

    def move(self):
        if self.y < self.target_y:
            self.y += self.speed
        elif self.y > self.target_y:
            self.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 30, 30))

# Oyun döngüsü
running = True
data_blocks = []
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    
    # Bellek seviyelerini çiz
    pygame.draw.rect(screen, RED, (100, levels["Register"], 600, 50))
    pygame.draw.rect(screen, BLUE, (100, levels["Cache"], 600, 50))
    pygame.draw.rect(screen, GREEN, (100, levels["RAM"], 600, 50))
    pygame.draw.rect(screen, GRAY, (100, levels["Disk"], 600, 50))
    
    font = pygame.font.Font(None, 36)
    screen.blit(font.render("Register", True, WHITE), (350, levels["Register"] + 10))
    screen.blit(font.render("Cache", True, WHITE), (350, levels["Cache"] + 10))
    screen.blit(font.render("RAM", True, WHITE), (350, levels["RAM"] + 10))
    screen.blit(font.render("Disk", True, WHITE), (350, levels["Disk"] + 10))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Space tuşuna basınca yeni veri ekle
                new_data = DataBlock(random.randint(120, 650), levels["Register"], random.choice(list(levels.keys())))
                data_blocks.append(new_data)

    # Veri bloklarını hareket ettir ve çiz
    for block in data_blocks:
        block.move()
        block.draw()

    pygame.display.update()
    clock.tick(100)

pygame.quit()