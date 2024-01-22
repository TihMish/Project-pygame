import os
import sys

import pygame


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


FPS = 50
WIDTH, HEIGHT = 1000, 700
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 255))
clock = pygame.time.Clock()
STEP = 50



class btn:
    def __init__(self, x, y, color, text=''):
        self.x, self.y = x, y
        self.width, self.height = 200, 50
        self.color = color
        self.text = text

    def draw(self):
        # отрисовка кнопки на экране
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        if self.text:
            font = pygame.font.SysFont(None, 20)
            text = font.render(self.text, 1, (255, 255, 255))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                               self.y + (self.height / 2 - text.get_height() / 2)))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Cannot load image", name)
        raise SystemExit(message)
    # image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


tile_images = {
    'wall': load_image('box.png'),
    'grass': load_image('grass.png'),
    'floor': load_image('flor.png'),
    'wall1': load_image('stenaVeth.png'),
    'wall2': load_image('stena.png'),
    'dorLV': load_image('dorLV.png'),
    'dorLN': load_image('dorLN.png'),
    'dorPV': load_image('dorPV.png'),
    'dorPN': load_image('dorPN.png'),
    'camen': load_image('camen.png'),
    'CamenLi': load_image('CamenLi.png'),
    'CamenLi1': load_image('CamenLi1.png'),
    'CamenLi2': load_image('CamenLi2.png'),
    'CamenLi20': load_image('CamenLi20.png'),
    'dorDPN': load_image('dorDPN.png'),
    'dorDLN': load_image('dorDLN.png')
}
tile_width = tile_height = 50
player_image = pygame.transform.scale(load_image("blcat.png"), (50, 50))

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def start_screen():
    intro_text = ["""Хождения Котейки
    Собери все вкусняшки
    Побывай везде"""]

    fon = pygame.transform.scale(load_image('FonC.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


def load_level(file_map):
    file_map = "data/" + file_map
    with open(file_map, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


camera = Camera()


def generate_level_out(level):  # Будет дороботка переходов и создание 2 разных полей(дом, улица)
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == '#':
                Tile('wall1', x, y)
            elif level[y][x] == '%':
                Tile('wall2', x, y)
            elif level[y][x] == '<':
                Tile('dorLV', x, y)
            elif level[y][x] == '&':
                Tile('camen', x, y)
            elif level[y][x] == '/':
                Tile('dorLN', x, y)
            elif level[y][x] == '>':
                Tile('dorPV', x, y)
            elif level[y][x] == '|':
                Tile('dorPN', x, y)
            elif level[y][x] == '+':
                Tile('CamenLi', x, y)
            elif level[y][x] == '-':
                Tile('CamenLi1', x, y)
            elif level[y][x] == '~':
                Tile('CamenLi2', x, y)
            elif level[y][x] == '_':
                Tile('CamenLi20', x, y)
            elif level[y][x] == '@':
                Tile('grass', x, y)
                new_player = Player(x, y)
        # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def generate_level_in(level):  # Будет дороботка переходов и создание 2 разных полей(дом, улица)
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('floor', x, y)
            elif level[y][x] == '#':
                Tile('wall1', x, y)
            elif level[y][x] == '%':
                Tile('wall2', x, y)
            elif level[y][x] == '<':
                Tile('dorLV', x, y)
            elif level[y][x] == '/':
                Tile('dorLN', x, y)
            elif level[y][x] == '>':
                Tile('dorPV', x, y)
            elif level[y][x] == '|':
                Tile('dorPN', x, y)
            elif level[y][x] == '@':
                Tile('floor', x, y)
                new_player = Player(x, y)
        # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def load_home(file_map):
    player, level_x, level_y = generate_level_in(load_level(file_map))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.rect.x -= STEP
                if event.key == pygame.K_RIGHT:
                    player.rect.x += STEP
                if event.key == pygame.K_UP:
                    player.rect.y -= STEP
                if event.key == pygame.K_DOWN:
                    player.rect.y += STEP
        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.fill("pink")
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def load_out(file_map):
    player, level_x, level_y = generate_level_out(load_level(file_map))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.rect.x -= STEP
                if event.key == pygame.K_RIGHT:
                    player.rect.x += STEP
                if event.key == pygame.K_UP:
                    player.rect.y -= STEP
                if event.key == pygame.K_DOWN:
                    player.rect.y += STEP
        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.fill("pink")
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def ch_home_out():
    disp = pygame.transform.scale(load_image('fon_ch.png'), (1050, 748))
    screen.blit(disp, (0, 0))
    home = btn(150, 180, (23, 38, 29), 'Home')
    out = btn(150, 280, (23, 38, 29), 'Out')
    home.draw()
    out.draw()
    font = pygame.font.Font(None, 30)
    text = font.render("Выберите место появления", True, (0, 0, 0))
    screen.blit(text, (100, 50))
    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                terminate()
            elif i.type == pygame.MOUSEBUTTONDOWN:
                p = pygame.mouse.get_pos()
                if home.x < p[0] < home.x + home.width and home.y < p[1] < home.y + home.height:
                    load_home('in.txt')
                elif out.x < p[0] < out.x + out.width and out.y < p[1] < out.y + out.height:
                    load_out('out.txt')

        pygame.display.flip()
        clock.tick(FPS)


ch_home_out()