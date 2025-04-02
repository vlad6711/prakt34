import pygame
import random
import sys

pygame.init()

window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Аркада v1.0")


def load_image(name, scale=1):
    try:
        image = pygame.image.load(name)
        if scale != 1:
            size = image.get_size()
            image = pygame.transform.scale(image, (int(size[0] * scale), int(size[1] * scale)))
        return image
    except pygame.error as e:
        print(f"Не удалось загрузить картинку: {name}")
        surface = pygame.Surface((50, 50))
        surface.fill((255, 0, 0) if "enemy" in name else (0, 255, 0) if "valorant" in name else (0, 0, 255))
        return surface


background_img = load_image('fon.jpg')
background_img = pygame.transform.scale(background_img, (window_width, window_height))
background_offset = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('valorant.png', 0.1)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 8

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        self.rect.x = max(0, min(self.rect.x, window_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, window_height - self.rect.height))


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('enemy.png', 0.2)
        self.rect = self.image.get_rect()
        self.reset_position()
        self.speedy = random.randrange(1, 5)
        self.speedx = random.randrange(-2, 2)

    def reset_position(self):
        self.rect.x = random.randrange(window_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > window_height + 10 or self.rect.left < -25 or self.rect.right > window_width + 25:
            self.reset_position()


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('arrow.png', 0.1)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
arrows = pygame.sprite.Group()

hero = Player(window_width / 2, window_height - 50)
all_sprites.add(hero)

for i in range(2):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

clock = pygame.time.Clock()
running = True
score = 0
font = pygame.font.SysFont('Arial', 36)

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                arrow = Arrow(hero.rect.centerx, hero.rect.top)
                arrows.add(arrow)
                all_sprites.add(arrow)

    all_sprites.update()

    hits = pygame.sprite.groupcollide(enemies, arrows, True, True)
    for hit in hits:
        score += 10
        new_enemy = Enemy()
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)

    if pygame.sprite.spritecollide(hero, enemies, False):
        running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        background_offset = (background_offset + 5) % window_width
    elif keys[pygame.K_RIGHT]:
        background_offset = (background_offset - 5) % window_width

    window.blit(background_img, (background_offset, 0))
    if background_offset != 0:
        window.blit(background_img, (background_offset - window_width, 0))

    all_sprites.draw(window)

    score_text = font.render(f'Счет: {score}', True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()