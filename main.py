import random
import sys

import pygame

pygame.init()


WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")


clock = pygame.time.Clock()


player_img = pygame.image.load("assets/player.png")
enemy_img = pygame.image.load("assets/enemy.png")
bullet_img = pygame.image.load("assets/bullet.png")


font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 8)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()


def show_menu():
    screen.fill(BLACK)
    draw_text(screen, "Space Shooter", 55, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type == pygame.KEYUP:
                waiting = False


def show_pause_menu():
    screen.fill(BLACK)
    draw_text(screen, "Pausa", 55, WIDTH // 2, HEIGHT // 2 - 100)
    draw_text(screen, "Presiona 'R' para reiniciar", 25, WIDTH // 2, HEIGHT // 2 - 20)
    draw_text(screen, "Presiona 'C' para continuar", 25, WIDTH // 2, HEIGHT // 2 + 20)
    draw_text(screen, "Presiona 'Q' para salir", 25, WIDTH // 2, HEIGHT // 2 + 60)
    pygame.display.flip()


def show_game_over():
    screen.fill(BLACK)
    draw_text(screen, "Game Over", 55, WIDTH // 2, HEIGHT // 2 - 100)
    draw_text(screen, "Presiona cualquier tecla para reiniciar", 25, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type == pygame.KEYUP:
                waiting = False
                main()  # Reinicia el juego


def main():
    global all_sprites, bullets

  
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    
   
    player = Player()
    all_sprites.add(player)
    
 
    for i in range(4):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

  
    score = 0

    running = True
    paused = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_SPACE:
                    player.shoot()
                if paused:
                    if event.key == pygame.K_r:
                        main()  
                    if event.key == pygame.K_c:
                        paused = False  
                    if event.key == pygame.K_q:
                        pygame.quit()  
        
        if not paused:
            all_sprites.update()
            
           
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                score += 50
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)
            
            # Colisiones entre enemigos y el jugador
            hits = pygame.sprite.spritecollide(player, enemies, False)
            if hits:
                show_game_over()
                running = False
            
            screen.fill(BLACK)
            all_sprites.draw(screen)
            draw_text(screen, f"Score: {score}", 18, WIDTH // 2, 10)
            pygame.display.flip()
        else:
            show_pause_menu()
    
    pygame.quit()


show_menu()
main()
