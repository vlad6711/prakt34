import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Аркада v1.0")


# Загрузка изображений
def load_image(name, scale=1):
    try:
        image = pygame.image.load(name)
        if scale != 1:
            size = image.get_size()
            image = pygame.transform.scale(image, (int(size[0] * scale), int(size[1] * scale)))
        return image
    except pygame.error as e:
        print(f"Cannot load image: {name}")
        # Заглушка, если изображение не найдено
        surface = pygame.Surface((50, 50))
        surface.fill((255, 0, 0) if "enemy" in name else (0, 255, 0) if "valorant" in name else (0, 0, 255))
        return surface


# Загрузка фона
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

        # Границы экрана
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

        # Если враг ушел за границы
        if self.rect.top > window_height + 10 or self.rect.left < -25 or self.rect.right > window_width + 25:
            self.reset_position()


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('arrow.png', 0.1)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10  # Стрела летит вверх

    def update(self):
        self.rect.y += self.speed
        # Удалить, если стрела вышла за границы экрана
        if self.rect.bottom < 0:
            self.kill()


# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
arrows = pygame.sprite.Group()

# Создание игрока
hero = Player(window_width / 2, window_height - 50)
all_sprites.add(hero)

# Создание врагов
for i in range(2):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Игровой цикл
clock = pygame.time.Clock()
running = True
score = 0
font = pygame.font.SysFont('Arial', 36)

while running:
    # Ограничение FPS
    clock.tick(60)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Создание новой стрелы
                arrow = Arrow(hero.rect.centerx, hero.rect.top)
                arrows.add(arrow)
                all_sprites.add(arrow)

    # Обновление спрайтов
    all_sprites.update()

    # Проверка столкновений стрел с врагами
    hits = pygame.sprite.groupcollide(enemies, arrows, True, True)
    for hit in hits:
        score += 10
        # Создание нового врага вместо уничтоженного
        new_enemy = Enemy()
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)

    # Проверка столкновения игрока с врагами
    if pygame.sprite.spritecollide(hero, enemies, False):
        running = False

    # Движение фона
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        background_offset = (background_offset + 5) % window_width
    elif keys[pygame.K_RIGHT]:
        background_offset = (background_offset - 5) % window_width

    # Отрисовка
    window.blit(background_img, (background_offset, 0))
    if background_offset != 0:
        window.blit(background_img, (background_offset - window_width, 0))

    all_sprites.draw(window)

    # Отображение счета
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    pygame.display.flip()

# Завершение игры
pygame.quit()
sys.exit()