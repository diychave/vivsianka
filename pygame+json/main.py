import pygame
import json
import os

pygame.init()

# Настройки экрана
width = 800
height = 800
tile_size = 40

# Переменные игры
game_over = 0
level = 1
max_level = 4
fps = 60

# Создание окна
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gopluck")

# Загрузка фона
bg_image = pygame.image.load('bg8/bg8.png')
bg_rect = bg_image.get_rect()

# Группы спрайтов
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# Функция загрузки уровня
def load_level(level):
    level_path = f'levels/level{level}.json'
    if not os.path.exists(level_path):
        print(f"Ошибка: файл {level_path} не найден!")
        return None
    try:
        with open(level_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON в файле {level_path}")
        return None

# Функция сброса уровня
def reset_level(start_from_first=False):
    """Сбрасывает уровень, при необходимости начиная с первого."""
    global world, game_over, level
    if start_from_first:
        level = 1  # Сброс до первого уровня
    player.reset_position()
    world_data = load_level(level)
    world = World(world_data) if world_data else None
    game_over = 0


class Player():
    def __init__(self):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        for num in range(1, 3):
            img_right = pygame.image.load(f'bg8/player{num}.png')
            img_right = pygame.transform.scale(img_right, (35, 60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.reset_position()

        self.gravity = 0
        self.jumped = False
        self.direction = 0
        self.dead_image = pygame.image.load('bg8/ghoust.png')

    def reset_position(self):
        """Респавн игрока"""
        self.rect.x = 100
        self.rect.y = height - 130

    def update(self):
        global game_over, level
        x = 0
        y = 0
        walk_speed = 10

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jumped:
                self.gravity = -15
                self.jumped = True

            if key[pygame.K_LEFT]:
                x -= 5
                self.direction = -1
                self.counter += 1
            if key[pygame.K_RIGHT]:
                x += 5
                self.direction = 1
                self.counter += 1

            if self.counter > walk_speed:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images_right)
                self.image = self.images_right[self.index] if self.direction == 1 else self.images_left[self.index]

            # Гравитация
            self.gravity += 1.3
            self.gravity = min(self.gravity, 10)
            y += self.gravity

            # Проверка столкновений
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + x, self.rect.y, self.rect.width, self.rect.height):
                    x = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + y, self.rect.width, self.rect.height):
                    if self.gravity < 0:
                        y = tile[1].bottom - self.rect.top
                        self.gravity = 0
                    else:
                        y = tile[1].top - self.rect.bottom
                        self.gravity = 0
                        self.jumped = False

            # Обновление координат игрока
            self.rect.x += x
            self.rect.y += y

            if self.rect.bottom > height:
                self.rect.bottom = height

            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1  # Игрок умер

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1  # Игрок прошел уровень

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 0:
                self.rect.y -= 5

        display.blit(self.image, self.rect)

class Button:
    def __init__(self, x, y, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self):
        action = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                action = True
        display.blit(self.image, self.rect)
        return action

restart_button = Button(width // 2, height // 2, "bg8/restart_btn_2.png")
start_button = Button(width // 2 + 150, height // 2 + 50, "bg8/start_btn_2.png")
exit_button = Button(width // 2 - 150, height // 2 + 50, "bg8/exit_btn_2.png")

class World():
    def __init__(self, data):
        self.tile_list = []
        dirt_img = pygame.image.load('bg8/tile3.png')
        grass_img = pygame.image.load('bg8/tile4.png')

        for row_index, row in enumerate(data):
            for col_index, tile in enumerate(row):
                if tile in (1, 2):
                    img = pygame.transform.scale(dirt_img if tile == 1 else grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect(topleft=(col_index * tile_size, row_index * tile_size))
                    self.tile_list.append((img, img_rect))
                elif tile == 3:
                    lava_group.add(Lava(col_index * tile_size, row_index * tile_size + tile_size // 2))
                elif tile == 5:
                    exit_group.add(Exit(col_index * tile_size, row_index * tile_size - tile_size / 2))

    def draw(self):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('bg8/exit.png'), (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect(topleft=(x, y))

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('bg8/lava.png'), (tile_size, tile_size // 2))
        self.rect = self.image.get_rect(topleft=(x, y))

player = Player()
world_data = load_level(level)
world = World(world_data) if world_data else None

run = True
main_menu = True
clock = pygame.time.Clock()

while run:
    clock.tick(fps)
    display.blit(bg_image, bg_rect)

    if main_menu:
        if start_button.draw():
            main_menu = False
            reset_level()
        if exit_button.draw():
            run = False
    else:
        player.update()
        world.draw()
        lava_group.draw(display)
        exit_group.draw(display)

        if game_over == -1:
            if restart_button.draw():
                reset_level(start_from_first=True)

        elif game_over == 1:
            level += 1
            if level <= max_level:
                reset_level()
            else:
                main_menu = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
