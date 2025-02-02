import pygame
from pygame import *
import sys

font.init()
WIGHT = 1200
HEIGHT = 700
SIZE = (WIGHT, HEIGHT)
TABLO = 50

mas_answer1_wight_l = 50
mas_answer1_wight_r = 149
mas_answer1_height_l = HEIGHT // 2 + 100
mas_answer1_height_r = mas_answer1_height_l + 49
mas_answer2_wight_l = 250
mas_answer2_wight_r = mas_answer2_wight_l + 99
mas_answer2_height_l = HEIGHT // 2 + 100
mas_answer2_height_r = mas_answer2_height_l + 49
mas_rest_height_l = WIGHT - 240
mas_rest_height_r = mas_rest_height_l + 119
mas_rest_wight_l = 10
mas_rest_wight_r = mas_rest_wight_l + 49
mas_help_wight_l = WIGHT - 110
mas_help_wight_r = mas_help_wight_l + 99
mas_help_height_l = 10
mas_help_height_r = mas_help_height_l + 49
window = pygame.display.set_mode((SIZE[0], SIZE[1]))
SCREEN_SIZE = pygame.Rect((0, 0, WIGHT, HEIGHT))
pygame.display.set_caption('Lost in Forest')
try:
    logo = pygame.image.load('data/logotip.png')
    pygame.display.set_icon(logo)
except pygame.error as e:
    print(f"Ошибка загрузки логотипа: {e}")

TILE_SIZE = 40
with open('data/level1.txt', 'r') as file:
    level1 = [line for line in file]
with open('data/level2.txt', 'r') as file:
    level2 = [line for line in file]
level = level1
# шрифты
myfont = pygame.font.SysFont('arial', 31)
myfont1 = pygame.font.SysFont('colibri', 28)
myfont2 = pygame.font.SysFont('arial', 28, italic=True)
myfont3 = pygame.font.SysFont('arial', 26, italic=True)
myfont_vybor = pygame.font.SysFont('arial', 28, bold=True)
GRAVITY = pygame.Vector2((0, 0.3))


# классы
class Entity(pygame.sprite.Sprite):
    def __init__(self, color, pos, *groups):
        super().__init__(*groups)
        self.image = Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)


class Player(Entity):
    MainEkran = True
    vstrecha = 0
    mon = 0
    mon2 = 0
    vopros = 0
    jk = False
    lava_death = False
    is_game = False
    pers = 2
    ikonka = 0
    level_count = 1
    answer1 = ''
    answer2 = ''
    question1 = ''
    question2 = ''
    question3 = ''
    question4 = ''
    question5 = ''
    question6 = ''
    isexit = False

    def __init__(self, platforms, pos, *groups):
        super().__init__(Color("#0000FF"), pos)
        try:
            if Player.pers == 1:
                self.image = pygame.image.load('data/stepright1.jpg')
                self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
                self.image.set_colorkey((255, 255, 255))
            elif Player.pers == 3:
                self.image = pygame.image.load('data/face' + str(Player.pers) + '.png')
                self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
                self.image.set_colorkey((255, 255, 255))
            else:
                self.image = pygame.image.load('data/face2.jpg')
                self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
                self.image.set_colorkey((0, 0, 0))
        except pygame.error as e:
            print(f"Ошибка загрузки изображения персонажа: {e}")
            self.image.fill(Color("#0000FF"))
        self.vel = pygame.Vector2((0, 0))
        self.onGround = False
        self.platforms = platforms
        self.speed = 8
        self.jump_strength = 10

    # обрабатываем действия
    def update(self):
        pressed = pygame.key.get_pressed()
        up = pressed[K_UP]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]
        running = pressed[K_SPACE]
        W1 = pressed[K_w]
        A1 = pressed[K_a]
        D1 = pressed[K_d]
        if Player.MainEkran:
            if up or W1:
                if self.onGround:
                    self.vel.y = -self.jump_strength
            if left or A1:
                self.vel.x = -self.speed
                if Player.pers != 2:
                    if Player.pers == 1:
                        self.image = pygame.image.load('data/stepright' + str((Player.ikonka // 11) % 3 + 1) + '.jpg')
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
                        self.image.set_colorkey((255, 255, 255))
                    elif Player.pers == 3:
                        self.image = pygame.image.load('data/girlstepright' + str((Player.ikonka // 11) % 3 + 1) + '.png')
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
                        self.image.set_colorkey((255, 255, 255))
                else:
                    self.image = pygame.image.load('data/2stepright' + str((Player.ikonka // 11) % 2 + 1) + '.jpg')
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
                    self.image.set_colorkey((0, 0, 0))
            if right or D1:
                self.vel.x = self.speed
                if Player.pers != 2:
                    if Player.pers == 1:
                        self.image = pygame.image.load('data/stepright' + str((Player.ikonka // 11) % 3 + 1) + '.jpg')
                        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
                        self.image.set_colorkey((255, 255, 255))
                    if Player.pers == 3:
                        self.image = pygame.image.load('data/girlstepright' + str((Player.ikonka // 11) % 3 + 1) + '.png')
                        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
                        self.image.set_colorkey((255, 255, 255))
                else:
                    self.image = pygame.image.load('data/2stepright' + str((Player.ikonka // 11) % 2 + 1) + '.jpg')
                    self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
                    self.image.set_colorkey((0, 0, 0))
            if running:
                self.vel.x *= 1.5
            if not self.onGround:
                self.vel += GRAVITY
                if self.vel.y > 100: self.vel.y = 100
            if not (left or right or D1 or A1):
                self.vel.x = 0
                if self.onGround:
                    if Player.pers == 3:
                        self.image = pygame.image.load('data/face' + str(Player.pers) + '.png')
                        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
                        self.image.set_colorkey((255, 255, 255))
                    elif Player.pers == 1:
                        pass
                    else:
                        self.image = pygame.image.load('data/face2.jpg')
                        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
                        self.image.set_colorkey((0, 0, 0))
            self.rect.left += self.vel.x
            self.collide(self.vel.x, 0, self.platforms)
            self.rect.top += self.vel.y
            self.onGround = False
            self.collide(0, self.vel.y, self.platforms)

    # прописываем столкновения объектов
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                # прописываем столкновения с дверью
                if isinstance(p, ExitBlock1) or isinstance(p, ExitBlock2):
                    Player.isexit = True
                if isinstance(p, LavaBlock):
                    Player.lava_death = True
                # прописываем столкновения с торговцами
                if isinstance(p, Torg1) or isinstance(p, Torg2):
                    platforms.remove(p)
                    if isinstance(p, Torg2):
                        Player.question1 = 'Недавно вы участвовали в онлайн-викторине и выиграли 3000 рублей.'
                        Player.question2 = 'Чтобы получить приз, нужно оплатить комиссию за перевод денег — 30 рублей.'
                        Player.question3 = 'Вот ссылка *** на страницу, где надо ввести все данные карты для оплаты.'
                        Player.question4 = 'По этим же реквизитам должны начислить вознаграждение.'
                        Player.question5 = ''
                        Player.question6 = ''
                        Player.answer1 = 'Верю'
                        Player.answer2 = 'Не верю!'
                        Player.vstrecha = 1
                        Player.vopros = 0
                        Player.MainEkran = False
                if isinstance(p, Torg3) or isinstance(p, Torg4):
                    platforms.remove(p)
                    if isinstance(p, Torg4):
                        Player.question1 = 'Добрый день. Я являюсь представителем официального банка.'
                        Player.question2 = 'В данный момент мошенники пытаются вздомать ваш личный кабинет.'
                        Player.question3 = 'Чтобы защитить деньги, надо скорее перевести их на безопасный резервный счет.'
                        Player.question4 = '**Со знакомого номера банка приходит СМС о заявке на резервирование счета.**'
                        Player.question5 = 'Для верификации и подтверждения заявки сообщите номер, срок действия карты '
                        Player.question6 = 'А так же три цифры с ее обратной стороны.'
                        Player.answer1 = 'Конечно!'
                        Player.answer2 = 'Это ложь'
                        Player.vstrecha = 2
                        Player.vopros = 0
                        Player.MainEkran = False
                if isinstance(p, Torg5) or isinstance(p, Torg6):
                    platforms.remove(p)
                    if isinstance(p, Torg6):
                        Player.question1 = 'Здравствуйте! Я хотел бы рассказать вам о том,'
                        Player.question2 = 'что недавно успешно инвестировал в компанию, которая вкладывается в перспективные'
                        Player.question3 = 'зарубежные стартапы в сфере технологий искусственного интеллекта.'
                        Player.question4 = 'Минимальный пакет акций стоит 10000 рублей и гарантирует 45% прибыли.'
                        Player.question5 = 'За каждого приведенного друга можно получить еще 5%. Я заработал уже 70000руб.'
                        Player.question6 = 'Предлагаю и вам стать инвестором — купить хотя бы стартовый пакет акций.'
                        Player.answer1 = 'Хорошо'
                        Player.answer2 = 'Не верю!'
                        Player.vstrecha = 3
                        Player.vopros = 0
                        Player.MainEkran = False

                if isinstance(p, Money):
                    if Player.level_count == 1:
                        Player.mon += 1
                        Money_SOUND = pygame.mixer.Sound("data/MarioMoney.wav")
                        pygame.mixer.Sound.play(Money_SOUND)
                    elif Player.level_count == 2:
                        Player.mon2 += 1
                        Money_SOUND = pygame.mixer.Sound("data/MarioMoney.wav")
                        pygame.mixer.Sound.play(Money_SOUND)
                    p.kill()
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.vel.y = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom


class Button:
    def __init__(self, x, y, width, height, text, normal_color, hover_color, text_color, font_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.font = self._load_font()
        self.image = self._render_text()
        self.hovered = False

    def _load_font(self):
        fonts = ["arial", "helvetica", "sans-serif", "times new roman"]
        for font_name in fonts:
            try:
                return pygame.font.SysFont(font_name, self.font_size)
            except pygame.error:
                pass
        print("Предупреждение: Ни один из указанных шрифтов не найден. Используется системный шрифт по умолчанию.")
        return pygame.font.Font(None, self.font_size)

    def _render_text(self):
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        surface.fill(self.normal_color)
        surface.blit(text_surface, text_rect)
        return surface

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.normal_color
        if list(color) != list(self.image.get_at((0, 0))[:3]):
            surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            surface.fill(color)
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
            surface.blit(text_surface, text_rect)
            self.image = surface
        screen.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

    def get_cords(self):
        return self.x, self.y, self.width + self.x, self.height + self.y


# объекты
class Platform(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#DDDDDD"), pos, *groups)
        try:
            self.image = pygame.image.load('data/Rock.png')
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        except pygame.error as e:
            print(f"Ошибка загрузки изображения платформы: {e}")


class ExitBlock1(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        try:
            self.image = pygame.image.load('data/door(1).png')
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        except pygame.error as e:
            print(f"Ошибка загрузки изображения ExitBlock1: {e}")


class ExitBlock2(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        try:
            self.image = pygame.image.load('data/door(2).png')
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        except pygame.error as e:
            print(f"Ошибка загрузки изображения ExitBlock2: {e}")


class Leaves(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        try:
            self.image = pygame.image.load('data/List.gif')
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            self.image.set_colorkey((0, 0, 0))
        except pygame.error as e:
            print(f"Ошибка загрузки изображения Leaves: {e}")


class Derevo(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        try:
            self.image = pygame.image.load('data/Der.png')
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        except pygame.error as e:
            print(f"Ошибка загрузки изображения Derevo: {e}")


class PerevDer(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        try:
            self.image = pygame.image.load('data/PerevDer.png')
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        except pygame.error as e:
            print(f"Ошибка загрузки изображения PerevDer: {e}")


class Money(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        try:
            self.image = pygame.image.load('data/money.png').convert()
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            self.image.set_colorkey((0, 0, 0))
        except pygame.error as e:
            print(f"Ошибка загрузки изображения Money: {e}")


class Torg1(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        self.image = pygame.image.load('data/Torg(5).png').convert()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey((0, 0, 0))


class Torg2(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        self.image = pygame.image.load('data/Torg(8).png').convert()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey((0, 0, 0))


class Torg3(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        self.image = pygame.image.load('data/Torg(5).png').convert()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey((0, 0, 0))


class Torg4(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        self.image = pygame.image.load('data/Torg(8).png').convert()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey((0, 0, 0))


class Torg5(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        self.image = pygame.image.load('data/Torg(5).png').convert()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey((0, 0, 0))


class Torg6(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        self.image = pygame.image.load('data/Torg(8).png').convert()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey((0, 0, 0))


class Stump(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        try:
            self.image = pygame.image.load('data/Pen(3).png').convert()
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            self.image.set_colorkey((0, 0, 0))
        except pygame.error as e:
            print(f"Ошибка загрузки изображения Stump: {e}")


class LavaBlock(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        try:
            self.image = pygame.image.load('data/lava.png').convert()
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            self.image.set_colorkey((0, 0, 0))
        except pygame.error as e:
            print(f"Ошибка загрузки изображения LavaBlock: {e}")


# прорисовка кадров
class CameraAwareLayeredUpdates(pygame.sprite.LayeredUpdates):
    def __init__(self, target, world_size):
        super().__init__()
        self.target = target
        self.cam = pygame.Vector2(0, 0)
        self.world_size = world_size
        if self.target:
            self.add(target)

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + SCREEN_SIZE.width / 2
            y = -self.target.rect.center[1] + SCREEN_SIZE.height / 2
            self.cam += (pygame.Vector2((x, y)) - self.cam) * 0.05
            self.cam.x = max(-(self.world_size.width - SCREEN_SIZE.width), min(0, self.cam.x))
            self.cam.y = max(-(self.world_size.height - SCREEN_SIZE.height), min(0, self.cam.y))

    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect
        for spr in self.sprites():
            rec = spritedict[spr]
            newrect = surface_blit(spr.image, spr.rect.move(self.cam))
            if rec is init_rect:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[spr] = newrect
        return dirty


def main_level():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE.size)
    pygame.display.set_caption("Lost in Forest")
    # обрабатываем действия
    # музыка
    pygame.mixer.music.load('data/LESFON.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.pause()
    BUTTON_SOUND = pygame.mixer.Sound("data/Button.wav")

    bg = pygame.image.load('data/trees.jpg').convert()
    bg = pygame.transform.scale(bg, (WIGHT, HEIGHT))
    SIZE = (WIGHT, HEIGHT)

    first_screen = pygame.Surface((WIGHT, HEIGHT))
    final_screen = pygame.Surface((WIGHT, HEIGHT))
    first_screen_open = 1
    window = pygame.display.set_mode((SIZE[0], SIZE[1]))

    moneys = []

    timer = pygame.time.Clock()
    # рисуем уровень
    level = []
    with open('data/level1.txt', 'r') as file:
        level1 = [line for line in file]
    level = level1
    platforms = pygame.sprite.Group()
    player = Player(platforms, (TILE_SIZE * 2, HEIGHT - TILE_SIZE - 5))
    level_width = len(level[0]) * TILE_SIZE
    level_height = len(level) * TILE_SIZE
    entities = CameraAwareLayeredUpdates(player, pygame.Rect(0, 0, level_width, level_height))
    x = y = 0

    # прорисовываем уроввень
    for row in level:
        for col in row:
            if col == "P":
                Platform((x, y), platforms, entities)
            elif col == "E":
                ExitBlock1((x, y), platforms, entities)
            elif col == "B":
                ExitBlock2((x, y), platforms, entities)
            elif col == "L":
                Leaves((x, y), platforms, entities)
            elif col == "D":
                Derevo((x, y), platforms, entities)
            elif col == "S":
                Stump((x, y), platforms, entities)
            elif col == "$":
                Money((x, y), platforms, entities)
            elif col == "T":
                Torg1((x, y), platforms, entities)
            elif col == "G":
                Torg2((x, y), platforms, entities)
            elif col == "Y":
                Torg3((x, y), platforms, entities)
            elif col == "H":
                Torg4((x, y), platforms, entities)
            elif col == "N":
                PerevDer((x, y), platforms, entities)
            elif col == "U":
                Torg5((x, y), platforms, entities)
            elif col == "J":
                Torg6((x, y), platforms, entities)
            elif col == "N":
                PerevDer((x, y), platforms, entities)
            elif col == "K":
                LavaBlock((x, y), platforms, entities)

            x += TILE_SIZE
        y += TILE_SIZE
        x = 0
    first_screen_open = 1
    isfinish = 0

    # основной цикл
    while 1 and Player.level_count == 1:
        if Player.isexit:
            first_screen_open = 6
        for e in pygame.event.get():
            if e.type == QUIT or Player.level_count != 1:
                return

            if e.type == KEYDOWN and e.key == K_ESCAPE:
                return

            # обрабатываем действия мыши
            if e.type == MOUSEBUTTONDOWN:
                mouse_press = mouse.get_pos()
                if (mas_help_wight_l <= mouse_press[0] <= mas_help_wight_r and mas_help_height_l <=
                        mouse_press[1] <= mas_help_height_r):
                    first_screen_open = 3
                if (mas_rest_wight_l <= mouse_press[0] <= mas_rest_wight_r and mas_rest_height_l <= mouse_press[1]
                        <= mas_rest_height_r):
                    main_level()
                    Player.mon = 1

        if isfinish == 1:
            continue
        # кнопки
        key = pygame.key.get_pressed()
        if key[pygame.K_1] and first_screen_open == 1:
            first_screen_open = 2
        if key[pygame.K_2] and first_screen_open == 2:
            first_screen_open = 3
        if key[pygame.K_3] and first_screen_open == 3:
            if Player.is_game:
                first_screen_open = 5
            else:
                first_screen_open = 4
        if first_screen_open == 4:
            if key[pygame.K_i]:
                Player.pers = 1
                first_screen_open = 5
            elif key[pygame.K_y]:
                Player.pers = 2
                first_screen_open = 5
            elif key[pygame.K_m]:
                Player.pers = 3
                first_screen_open = 5
        if first_screen_open == 1:
            # музыка
            pygame.mixer.music.unpause()

            first_screen = pygame.Surface(SIZE)
            first_screen.fill((255, 255, 255))
            tx1 = "Легенда игры"
            tx2 = 'Игорь, Маша и Яша были лучшими друзьями. Они часто проводили время вместе, играя'
            tx3 = 'в футбол и гуляя по лесу. Однажды они решили исследовать дальнюю часть леса,'
            tx4 = 'о которой слышали много загадочных историй. Они шли всего несколько часов,'
            tx5 = 'когда заметили, что потеряли дорогу и не знают, как вернуться назад. Ребята решили '
            tx6 = 'не паниковать и пойти дальше. Но вскоре они поняли, что заблудились еще глубже...'
            question_field1 = myfont2.render(tx1, True, (0, 0, 0))
            question_field2 = myfont3.render(tx2, True, (0, 0, 0))
            question_field3 = myfont3.render(tx3, True, (0, 0, 0))
            question_field4 = myfont3.render(tx4, True, (0, 0, 0))
            question_field5 = myfont3.render(tx5, True, (0, 0, 0))
            question_field6 = myfont3.render(tx6, True, (0, 0, 0))
            first_screen.blit(question_field1, ((WIGHT - question_field1.get_width()) // 2, 50))
            first_screen.blit(question_field2, ((WIGHT - question_field2.get_width()) // 2, 120))
            first_screen.blit(question_field3, ((WIGHT - question_field3.get_width()) // 2, 170))
            first_screen.blit(question_field4, ((WIGHT - question_field4.get_width()) // 2, 220))
            first_screen.blit(question_field5, ((WIGHT - question_field5.get_width()) // 2, 270))
            first_screen.blit(question_field6, ((WIGHT - question_field6.get_width()) // 2, 320))

            width = 150
            height = 75

            tx0 = 'Далее!'
            field_tx0 = myfont.render(tx0, True, (255, 255, 255))
            button = pygame.Surface((width, height))

            x = (WIGHT - button.get_width()) // 2
            y = HEIGHT - 250

            click = pygame.mouse.get_pressed()
            mouse1 = pygame.mouse.get_pos()

            if x < mouse1[0] < x + width:
                if y < mouse1[1] < y + height:
                    button.fill((23, 204, 58))
                    if click[0] == 1:
                        pygame.mixer.Sound.play(BUTTON_SOUND)
                        pygame.time.delay(300)
                        first_screen_open = 2
                else:
                    button.fill((13, 162, 58))
            else:
                button.fill((13, 162, 58))

            first_screen.blit(button, (x, y))
            first_screen.blit(field_tx0, (x + (button.get_width() - field_tx0.get_width()) // 2,
                                          y + (button.get_height() - field_tx0.get_height()) // 2))
            window.blit(first_screen, (0, 0))

        elif first_screen_open == 2:
            first_screen = pygame.Surface(SIZE)
            first_screen.fill((255, 255, 255))
            tx1 = "Они начали перебираться через тернистые кусты и осторожно идти в поисках выхода."
            tx2 = 'Время шло, и все больше и больше они понимали, что это была ошибка. Вскоре они '
            tx3 = 'вышли на незнакомую поляну, на которой стояла табличка: "Вы попали в загадочный лес.'
            tx4 = 'На вашем пути будут попадаться монеты. Соберите как можно больше монет. Кроме того,'
            tx5 = 'вам будут встречаться мошенники и торговцы. Ваша задача отличить их друг от друга.'
            tx6 = 'А также не попасться на уловки мошенников. В противном случае вы будете терять свои монеты... '
            question_field1 = myfont3.render(tx1, True, (0, 0, 0))
            question_field2 = myfont3.render(tx2, True, (0, 0, 0))
            question_field3 = myfont3.render(tx3, True, (0, 0, 0))
            question_field4 = myfont3.render(tx4, True, (0, 0, 0))
            question_field5 = myfont3.render(tx5, True, (0, 0, 0))
            question_field6 = myfont3.render(tx6, True, (0, 0, 0))
            first_screen.blit(question_field1, ((WIGHT - question_field1.get_width()) // 2, 60))
            first_screen.blit(question_field2, ((WIGHT - question_field2.get_width()) // 2, 120))
            first_screen.blit(question_field3, ((WIGHT - question_field3.get_width()) // 2, 180))
            first_screen.blit(question_field4, ((WIGHT - question_field4.get_width()) // 2, 240))
            first_screen.blit(question_field5, ((WIGHT - question_field5.get_width()) // 2, 300))
            first_screen.blit(question_field6, ((WIGHT - question_field6.get_width()) // 2, 360))

            width = 150
            height = 75

            tx0 = 'Далее!'
            field_tx0 = myfont.render(tx0, True, (255, 255, 255))
            button = pygame.Surface((width, height))

            x = (WIGHT - button.get_width()) // 2
            y = HEIGHT - 250

            click = pygame.mouse.get_pressed()
            mouse1 = pygame.mouse.get_pos()

            if x < mouse1[0] < x + width:
                if y < mouse1[1] < y + height:
                    button.fill((23, 204, 58))
                    if click[0] == 1:
                        pygame.mixer.Sound.play(BUTTON_SOUND)
                        pygame.time.delay(300)
                        first_screen_open = 3
                else:
                    button.fill((13, 162, 58))
            else:
                button.fill((13, 162, 58))

            first_screen.blit(button, (x, y))
            first_screen.blit(field_tx0, (x + (button.get_width() - field_tx0.get_width()) // 2,
                                          y + (button.get_height() - field_tx0.get_height()) // 2))
            window.blit(first_screen, (0, 0))

        elif first_screen_open == 3:
            first_screen = pygame.Surface(SIZE)
            first_screen.fill((255, 255, 255))
            tx1 = "Правила"
            tx2 = '1) Для управления персонажем используйте стрелки или кнопки: WASD'
            tx3 = '2) Для того чтобы ускорить движение, зажмите пробел'
            tx4 = 'З) Ваша задача в итоге собрать как можно больше монет и найти дверь,'
            tx5 = 'ведущая к выходу из леса'
            tx6 = '4) Желаем вам удачи!'
            question_field1 = myfont.render(tx1, True, (0, 0, 0))
            question_field2 = myfont2.render(tx2, True, (0, 0, 0))
            question_field3 = myfont2.render(tx3, True, (0, 0, 0))
            question_field4 = myfont2.render(tx4, True, (0, 0, 0))
            question_field5 = myfont2.render(tx5, True, (0, 0, 0))
            question_field6 = myfont2.render(tx6, True, (0, 0, 0))
            first_screen.blit(question_field1, ((WIGHT - question_field1.get_width()) // 2, 50))
            first_screen.blit(question_field2, (150, 150))
            first_screen.blit(question_field3, (150, 200))
            first_screen.blit(question_field4, (150, 250))
            first_screen.blit(question_field5, (150, 300))
            first_screen.blit(question_field6, (150, 350))
            width = 150
            height = 75

            tx0 = 'Далее!'
            field_tx0 = myfont.render(tx0, True, (255, 255, 255))
            button = pygame.Surface((width, height))

            x = (WIGHT - button.get_width()) // 2
            y = HEIGHT - 250

            click = pygame.mouse.get_pressed()
            mouse1 = pygame.mouse.get_pos()

            if x < mouse1[0] < x + width:
                if y < mouse1[1] < y + height:
                    button.fill((23, 204, 58))
                    if click[0] == 1:
                        pygame.mixer.Sound.play(BUTTON_SOUND)
                        pygame.time.delay(300)
                        first_screen_open = 4
                        if Player.is_game:
                            first_screen_open = 5
                else:
                    button.fill((13, 162, 58))
            else:
                button.fill((13, 162, 58))

            first_screen.blit(button, (x, y))
            first_screen.blit(field_tx0, (x + (button.get_width() - field_tx0.get_width()) // 2,
                                          y + (button.get_height() - field_tx0.get_height()) // 2))
            window.blit(first_screen, (0, 0))
        elif first_screen_open == 4:
            first_screen = pygame.Surface(SIZE)
            vybor_fon = pygame.image.load('data/vybor_fon.jpg')
            vybor_fon = pygame.transform.scale(vybor_fon, (WIGHT, HEIGHT))
            screen.blit(first_screen, (0, 0))
            Vybor_field = myfont_vybor.render('Выберите персонажа:', True, (255, 255, 255))
            Igor_field1 = myfont_vybor.render('Игорь(I)', True, (255, 255, 255))
            Yasha_field1 = myfont_vybor.render('Яша(Y)', True, (255, 255, 255))
            Masha_field1 = myfont_vybor.render('Маша(M)', True, (255, 255, 255))

            Igor = pygame.image.load('data/stepright1.jpg')
            Igor.set_colorkey((255, 255, 255))
            Yasha = pygame.image.load('data/face2.jpg')
            Yasha.set_colorkey((0, 0, 0))
            Masha = pygame.image.load('data/face3.png')
            Masha.set_colorkey((255, 255, 255))
            Igor = pygame.transform.scale(Igor, (TILE_SIZE * 6, TILE_SIZE * 7))
            Yasha = pygame.transform.scale(Yasha, (TILE_SIZE * 6, TILE_SIZE * 6))
            Masha = pygame.transform.scale(Masha, (TILE_SIZE * 6, TILE_SIZE * 6))
            screen.blit(vybor_fon, (0, 0))
            screen.blit(Vybor_field, (WIGHT // 2 - 200, 20))
            screen.blit(Igor_field1, (100, 250))
            screen.blit(Yasha_field1, (500, 250))
            screen.blit(Masha_field1, (900, 250))
            screen.blit(Igor, (50, 300))
            screen.blit(Yasha, (450, 300))
            screen.blit(Masha, (850, 300))

            pygame.mixer.music.pause()
            pygame.mixer.music.load('data/M(1).wav')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.pause()
        elif first_screen_open == 5:
            Player.is_game = True
            pygame.mixer.music.unpause()
            entities.update()
            count = myfont.render(f'Монеты: {Player.mon}.', True, (255, 255, 255))
            question_field1 = myfont2.render(Player.question1, True, (255, 255, 255))
            question_field2 = myfont2.render(Player.question2, True, (255, 255, 255))
            question_field3 = myfont2.render(Player.question3, True, (255, 255, 255))
            question_field4 = myfont2.render(Player.question4, True, (255, 255, 255))
            question_field5 = myfont2.render(Player.question5, True, (255, 255, 255))
            question_field6 = myfont2.render(Player.question6, True, (255, 255, 255))

            answer_field1 = myfont1.render(Player.answer1, True, (255, 255, 255))
            answer_sur1 = pygame.Surface((100, 50))
            answer_sur1.fill((25, 255, 25))
            answer_field2 = myfont1.render(Player.answer2, True, (255, 255, 255))
            answer_sur2 = pygame.Surface((100, 50))
            answer_sur2.fill((255, 25, 25))
            screen.blit(bg, (0, 0))

            entities.draw(screen)
            screen.blit(count, (35, 15))

            help_surf = Surface((100, 50))
            help_surf.fill((0, 0, 0))
            help_surf.set_colorkey((0, 0, 0))
            help_field = myfont.render(('Help'), True, (255, 255, 255))
            screen.blit(help_surf, (WIGHT - 110, 10))
            screen.blit(help_field, (WIGHT - 95, 25))

            restart_surf = Surface((120, 50))
            restart_surf.fill((0, 0, 0))
            restart_surf.set_colorkey((0, 0, 0))
            restart_field = myfont.render(('Restart'), True, (255, 255, 255))
            screen.blit(restart_surf, (WIGHT - 240, 10))
            screen.blit(restart_field, (WIGHT - 230, 25))

            if Player.vstrecha != 0:
                les_fon = pygame.image.load('data/les_fon.png')
                les_fon = pygame.transform.scale(les_fon, (WIGHT, HEIGHT))
                torg_up = pygame.image.load('data/TorgUp.png')
                torg_up = pygame.transform.scale(torg_up, (TILE_SIZE * 4 + 15, TILE_SIZE * 4))
                torg_down = pygame.image.load('data/TorgDown.png')
                torg_down = pygame.transform.scale(torg_down, (TILE_SIZE * 4 + 15, TILE_SIZE * 4))
                if Player.pers != 2:
                    hero = pygame.image.load('data/face' + str(Player.pers) + '.png')
                    hero = pygame.transform.scale(hero, (TILE_SIZE * 4, TILE_SIZE * 4))
                    hero.set_colorkey((255, 255, 255))
                else:
                    hero = pygame.image.load('data/face2.jpg')
                    hero = pygame.transform.scale(hero, (TILE_SIZE * 4, TILE_SIZE * 4))
                    hero.set_colorkey((0, 0, 0))
                screen.blit(les_fon, (0, 0))
                screen.blit(torg_up, (800, 350))
                screen.blit(torg_down, (800, 350 + TILE_SIZE * 4))
                screen.blit(hero, (450, 478))
                screen.blit(count, (35, 15))
                screen.blit(question_field1, (40, 80))
                screen.blit(question_field2, (40, 130))
                screen.blit(question_field3, (40, 180))
                screen.blit(question_field4, (40, 230))
                screen.blit(question_field5, (40, 280))
                screen.blit(question_field6, (40, 330))
                mouse_press = mouse.get_pos()
                if Player.vopros == 1 and MOUSEBUTTONDOWN:
                    if mas_answer1_wight_l <= mouse_press[0] <= mas_answer1_wight_r and mas_answer1_height_l <= \
                            mouse_press[1] <= mas_answer1_height_r:
                        answer_sur1.fill((255, 165, 28))
                        screen.blit(answer_sur1, (50, HEIGHT // 2 + 100))
                        screen.blit(answer_field1, (60, HEIGHT // 2 + 15 + 100))
                    screen.blit(answer_sur1, (50, HEIGHT // 2 + 100))
                    screen.blit(answer_field1, (60, HEIGHT // 2 + 15 + 100))
                    Player.answer1 = "Далее!"
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            Player.vstrecha = 0
                            Player.question1 = ''
                            Player.question2 = ''
                            Player.question3 = ''
                            Player.question4 = ''
                            Player.question5 = ''
                            Player.question6 = ''
                            Player.answer1 = Player.answer2 = ''
                            Player.vopros = 0
                            Player.MainEkran = True
                else:
                    if mas_answer1_wight_l <= mouse_press[0] <= mas_answer1_wight_r and mas_answer1_height_l <= \
                            mouse_press[1] <= mas_answer1_height_r:
                        answer_sur1.fill((255, 165, 28))
                        screen.blit(answer_sur1, (50, HEIGHT // 2 + 100))
                        screen.blit(answer_field1, (60, HEIGHT // 2 + 15 + 100))
                        screen.blit(answer_sur2, (250, HEIGHT // 2 + 100))
                        screen.blit(answer_field2, (260, HEIGHT // 2 + 15 + 100))
                        if e.type == MOUSEBUTTONDOWN and Player.vstrecha == 2:
                            Player.question1 = 'Ну зачем же так сразу?!'
                            Player.question2 = 'Мошенники научились подделывать официальные номера банков и даже придумали,'
                            Player.question3 = 'как использовать настоящие СМС-рассылки банков в своих схемах.'
                            Player.question4 = 'Никому и никогда нельзя называть полные реквизиты карты, включая срок действия,'
                            Player.question5 = 'трехзначный код с обратной стороны, а также коды и пароли из уведомления'
                            Player.question6 = 'от банка. Если у вас просят эти данные — вы столкнулись с мошенниками.'
                            Player.answer1 = Player.answer2 = ''
                            Player.mon -= 1
                            Player.vopros = 1
                        elif e.type == MOUSEBUTTONDOWN and Player.vstrecha == 1:
                            Player.question1 = 'Упс!'
                            Player.question2 = 'Это мошенники. По ссылке для оплаты комиссии вы попадете на фишинговую'
                            Player.question3 = 'страницу — хакеры создали ее для того, чтобы заполучить данные вашей карты.'
                            Player.question4 = 'Если переведете аферистам 30 рублей, они смогут украсть гораздо больше.'
                            Player.question5 = ''
                            Player.question6 = ''
                            Player.answer1 = Player.answer2 = ''
                            Player.mon -= 1
                            Player.vopros = 1
                        elif e.type == MOUSEBUTTONDOWN and Player.vstrecha == 3:
                            Player.question1 = 'Кажется, вы поторопились с решением.'
                            Player.question2 = 'Это классическая финансовая пирамида. Организаторы обещают большую'
                            Player.question3 = 'доходность и бонусы за то, что вы приведете им новых вкладчиков. У таких компаний'
                            Player.question4 = 'нет ни лицензии, ни достоверных данных о регистрации, ни финансовой отчетности.'
                            Player.question5 = ''
                            Player.question6 = ''
                            Player.answer1 = Player.answer2 = ''
                            Player.mon -= 1
                            Player.vopros = 1


                    elif mas_answer2_wight_l <= mouse_press[0] <= mas_answer2_wight_r and mas_answer2_height_l <= \
                            mouse_press[1] <= mas_answer2_height_r:
                        answer_sur2.fill((255, 165, 28))
                        screen.blit(answer_sur2, (250, HEIGHT // 2 + 100))
                        screen.blit(answer_field2, (260, HEIGHT // 2 + 15 + 100))
                        screen.blit(answer_sur1, (50, HEIGHT // 2 + 100))
                        screen.blit(answer_field1, (60, HEIGHT // 2 + 15 + 100))
                        if e.type == MOUSEBUTTONDOWN and Player.vstrecha == 2:
                            Player.question1 = 'И это правильный ответ!'
                            Player.question2 = 'Никому и никогда нельзя называть полные реквизиты карты, включая срок действия,'
                            Player.question3 = 'трехзначный код с обратной стороны, а также коды и пароли из уведомления'
                            Player.question4 = 'от банка. Если у вас просят эти данные — вы столкнулись с мошенниками.'
                            Player.question5 = 'Они научились не только подделывать официальные номера банков,'
                            Player.question6 = 'но и использовать настоящие СМС-рассылки банков в своих схемах.'
                            Player.answer1 = Player.answer2 = ''
                            Player.mon += 1
                            Player.vopros = 1
                        elif e.type == MOUSEBUTTONDOWN and Player.vstrecha == 1:
                            Player.question1 = 'И правильно!'
                            Player.question2 = 'Мошенники использовали популярную схему обмана — «беспроигрышный'
                            Player.question3 = 'лохотрон». Если ввести данные карты на их фишинговой странице, то можно потерять'
                            Player.question4 = 'все деньги.'
                            Player.question5 = ''
                            Player.question6 = ''
                            Player.answer1 = Player.answer2 = ''
                            Player.mon += 1
                            Player.vopros = 1
                        elif e.type == MOUSEBUTTONDOWN and Player.vstrecha == 3:
                            Player.question1 = 'Грамотный ход.'
                            Player.question2 = 'Вас завлекают в классическую финансовую пирамиду. Организаторы'
                            Player.question3 = 'обещают большую доходность, за привлечение вкладчиков вы получаете бонусы.'
                            Player.question4 = 'У таких компаний нет ни лицензии, ни финансовой отчетности.'
                            Player.question5 = ''
                            Player.question6 = ''
                            Player.answer1 = Player.answer2 = ''
                            Player.mon += 1
                            Player.vopros = 1

                    else:
                        screen.blit(answer_sur1, (50, HEIGHT // 2 + 100))
                        screen.blit(answer_field1, (60, HEIGHT // 2 + 15 + 100))
                        screen.blit(answer_sur2, (250, HEIGHT // 2 + 100))
                        screen.blit(answer_field2, (260, HEIGHT // 2 + 15 + 100))
        elif first_screen_open == 6:
            txt1 = myfont.render(str("Молодец! Ты собрал ") + str(
                Player.mon) + " монеты и помог ребятам выйти из Загадочного леса!", True, (0, 0, 0))
            if Player.mon < 0:
                txt1 = myfont.render(f"По итогам игры ты ушел в долг на {-Player.mon}(", True, (0, 0, 0))
            if Player.mon < 3:
                txt2 = myfont.render("У вас не плохой результат, но вы можете лучше. Попробуйте ещё раз!", True,
                                     (0, 0, 0))
                txt3 = myfont.render("Вы моете усовершенствовать свои знания по финансовой грамоте на сайте:", True,
                                     (0, 0, 0))
                txt4 = myfont.render("https://fincult.info/", True, (0, 0, 0))

            elif Player.mon < 6:
                txt2 = myfont.render("У вас не плохой результат, но вы можете лучше. Попробуйте ещё раз.", True,
                                     (0, 0, 0))
                txt3 = myfont.render("Вы моете усовершенствовать свои знания по финансовой грамоте на сайте:", True,
                                     (0, 0, 0))
                txt4 = myfont.render("https://fincult.info/", True, (0, 0, 0))

            elif Player.mon <= 8:
                txt2 = myfont.render("Ваш результат превосходен. Продолжайте в том же духе!", True, (0, 0, 0))
                txt3 = myfont.render("Вы моете усовершенствовать свои знания по финансовой грамоте на сайте:", True,
                                     (0, 0, 0))
                txt4 = myfont2.render("https://fincult.info/", True, (0, 0, 0))

            final_screen = pygame.Surface(SIZE)
            final_screen.fill((255, 255, 255))
            image1 = pygame.image.load("data/QR code.png")

            final_screen.blit(txt1, (150, 150))
            final_screen.blit(txt2, (200, 200))
            final_screen.blit(txt3, (150, 250))
            final_screen.blit(txt4, (500, 300))
            image1.set_colorkey((0, 0, 0))
            image1 = pygame.transform.scale(image1, (200, 200))
            final_screen.blit(image1, (500, 350))

            screen.blit(final_screen, (0, 0))
            isfinish = 1
            pygame.display.update()
            timer.tick(60)
        Player.ikonka += 1
        pygame.display.update()
        timer.tick(60)


# запуск игры
if __name__ == "__main__":
    main_level()
