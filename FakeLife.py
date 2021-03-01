import pygame
from win32api import GetSystemMetrics


fps = 120
invent = 0
running = True
size = width, height = GetSystemMetrics(0), GetSystemMetrics(1)
button_sound, take_ground, give_ground, stay_on_ground = 0, 0, 0, 0
board = [list(i) for i in open("data/map/map.txt",
                               "r", encoding="utf-8").read().split("\n")]
bg = pygame.image.load("data/images/background.png")
surf_alpha = pygame.Surface((width, height))
c = 0
jump = True
but_v = True
pressed = False
x_pos, y_pos = ((width - 200) // 2, 772)
cell_size = 70
bx, by = (0, 0)
left, top = (-(cell_size * 50 - width) // 2, 0)
xr, yr1, yr2, xl, yl1, yl2 = 0, 0, 0, 0, 0, 0
b_board = 0


# ----------------------------OpeningTheMenu-----------------------------------


class Menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/images/menu.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = width - 150, 50

    def update(self):
        global but_v
        x, y = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.rect.x < x < self.rect.x + 100 + self.rect.x and \
                self.rect.y < y < self.rect.y + 100 + self.rect.y:
            if click[0] == 1:
                button_sound.play()
                but_v = True


# ---------------------------------Blocks--------------------------------------


class Terrain:
    def __init__(self):
        self.width = width
        self.height = height
        self.left, self.top = left, top
        self.cell_size = cell_size
        self.board = board
        self.grass = pygame.image.load("data/images/grass.png")
        self.grass_rect = self.grass.get_rect()
        self.grass_rect.x, self.grass_rect.y = self.left, self.top
        self.ground = pygame.image.load("data/images/ground.png")
        self.ground_rect = self.ground.get_rect()
        self.ground_rect.x, self.ground_rect.y = self.left, self.top

    def render(self, screen):
        global invent
        x, y = self.left, self.top
        for i in self.board:
            x = self.left
            for j in i:
                if int(j) == 1:
                    pygame.draw.rect(screen, (130, 173, 63),
                                     (x, y, self.cell_size - 1,
                                      self.cell_size - 1))
                    pygame.draw.rect(screen, (79, 104, 38),
                                     (x, y, self.cell_size, self.cell_size), 1)
                elif int(j) == 2:
                    pygame.draw.rect(screen, (116, 75, 32),
                                     (x, y, self.cell_size - 1,
                                      self.cell_size - 1))
                    pygame.draw.rect(screen, (86, 56, 24),
                                     (x, y, self.cell_size, self.cell_size), 1)
                elif int(j) == 6:
                    pygame.draw.rect(screen, (91, 193, 98),
                                     (x, y, self.cell_size - 1,
                                      self.cell_size - 1))
                    pygame.draw.rect(screen, (74, 157, 79),
                                     (x, y, self.cell_size, self.cell_size), 1)
                elif int(j) == 0:
                    pygame.draw.rect(screen, (172, 120, 78),
                                     (x, y, self.cell_size - 1,
                                      self.cell_size - 1))
                    pygame.draw.rect(screen, (92, 64, 42),
                                     (x, y, self.cell_size, self.cell_size), 1)
                elif int(j) == 4:
                    pygame.draw.rect(screen, (142, 141, 139),
                                     (x, y, self.cell_size - 1,
                                      self.cell_size - 1))
                    pygame.draw.rect(screen, (68, 68, 67),
                                     (x, y, self.cell_size, self.cell_size), 1)
                elif int(j) == 3:
                    co, co_v = 0, 0
                    for s in self.board[0:]:
                        for k in s:
                            if int(k) == 3:
                                co += 1
                    for e in self.board[:13]:
                        for g in e:
                            if int(g) == 0:
                                co_v += 1
                    invent = co - co_v
                x += self.cell_size
            y += self.cell_size

    def update(self):
        global invent, left, xr, yr1, yr2, xl, yl1, yl2, b_board
        key = pygame.key.get_pressed()
        _dir = 0
        x, y = pygame.mouse.get_pos()
        x1, y1 = (x - self.left) // cell_size, (y - top) // cell_size
        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            if int(self.board[int(y1)][int(x1)]) in (0, 1, 2, 6):
                self.board[int(y1)][int(x1)] = str(3)
                take_ground.play()
                invent += 1
        if click[2] == 1:
            if int(self.board[int(y1)][int(x1)]) in (3, 5):
                if invent > 0:
                    self.board[int(y1)][int(x1)] = str(0)
                    give_ground.play()
                    invent -= 1
        if key[pygame.K_RIGHT]:
            if self.left >= -((self.cell_size * 50) - self.width):
                if int(self.board[yr1][xr - 1]) in (5, 3, 2, 6) and int(
                        self.board[yr2][xr - 1]) in (5, 3, 2, 6):
                    self.left -= 15
                    left -= 15
        if key[pygame.K_LEFT]:
            if self.left < 0:
                if int(self.board[yl1][xl + 1]) in (5, 3, 2, 6) and int(
                        self.board[yl2][xl + 1]) in (5, 3, 2, 6):
                    self.left += 15
                    left += 15
        b_board = self.board


# ---------------------------------Person--------------------------------------


class Person(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.left = left
        self.cell_size = cell_size
        self.image = pygame.image.load("data/images/person_m.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x_pos, y_pos
        self.dir_j = 0
        self.dir = 0
        self.control = 0

    def update(self, screen):
        global left, top, board, xr, yr1, yr2, xl, yl1, yl2, b_board
        _dir = 0
        key = pygame.key.get_pressed()

        xd1, xd2, xd3 = (self.rect.x - left) // cell_size, \
                        (self.rect.x - left) // cell_size + 1, \
                        (self.rect.x - left) // cell_size + 2
        yd = (self.rect.y + top) // cell_size + 2
        xr = (self.rect.x - left + 138) // cell_size + 1
        yr1, yr2 = (self.rect.y + top) // cell_size, \
                   (self.rect.y + top) // cell_size + 1
        xl = (self.rect.x - left) // cell_size - 1
        yl1, yl2 = (self.rect.y + top) // cell_size, \
                   (self.rect.y + top) // cell_size + 1
        xu1, xu2, xu3 = (self.rect.x - left) // cell_size, \
                        (self.rect.x - left) // cell_size + 1, \
                        (self.rect.x - left) // cell_size + 2
        yu = (self.rect.y + top) // cell_size - 1

        if board[yd][xd1] in (str(3), str(5)) and board[yd][xd2] in \
                (str(3), str(5)) and board[yd][xd3] in (str(3), str(5)):
            self.rect.y += 10

        if self.dir_j == 1:
            self.jump(xd1, xd2, xd3, yd, xu1, xu2, xu3, yu)

        if key[pygame.K_UP]:
            self.dir_j = 1

        if key[pygame.K_RIGHT]:
            if left < -((self.cell_size * 50) - width):
                if self.rect.x <= 200 + (self.cell_size * 50) - width:
                    if int(b_board[yr1][xr - 1]) in (5, 3, 2, 6) and int(
                            b_board[yr2][xr - 1]) in (5, 3, 2, 6):
                        self.rect.x += 10
            _dir = 0

        if key[pygame.K_LEFT]:
            if left >= 0:
                if self.rect.x >= left:
                    if int(b_board[yl1][xl + 1]) in (5, 3, 2, 6) and int(
                            b_board[yl2][xl + 1]) in (5, 3, 2, 6):
                        self.rect.x -= 10
            _dir = 1
        if _dir != self.dir:
            self.reverse()
            self.dir = _dir

    def jump(self, xd1, xd2, xd3, yd, xu1, xu2, xu3, yu):
        global jump
        if jump is True:
            if self.control < 350 and board[yu + 1][xu1] in \
                    (str(3), str(5), str(2), str(6)) and board[yu + 1][xu2] in\
                    (str(3), str(5), str(2), str(6)) and board[yu + 1][xu3] in\
                    (str(3), str(5), str(2), str(6)):
                self.rect.y -= 25
                self.control += 25
            else:
                jump = False
                self.control = 0
        else:
            if board[yd][xd1] in (str(3), str(5), str(2), str(6)) and \
                    board[yd][xd2] in (str(3), str(5), str(2), str(6)) and \
                    board[yd][xd3] in (str(3), str(5), str(2), str(6)):
                self.rect.y += 7
            else:
                self.dir_j = 0
                jump = True

    def reverse(self):
        self.image = pygame.transform.flip(self.image, True, False)


# ------------------------------MenuButtons------------------------------------


class Buttons:
    def __init__(self):
        self.time = 0
        self.timer = 68
        self.a = 6
        self.pressed = pressed
        self.width = 300
        self.height = 100
        self.x_start, self.y_start = (
            (width - self.width) // 2, (height - (self.height * 2 + 100)) // 2)
        self.x_output, self.y_output = (
            (width - self.width) // 2, (height - (self.height - 100)) // 2)
        self.color1, self.color = (16, 166, 109), (18, 184, 120)

    def render(self, screen):
        global running, width, height, c, bg, but_v, pressed
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        font = pygame.font.SysFont('American Captain Cyrillic', 80)
        text = font.render("Начать", 1, (80, 80, 80,))
        if self.x_start < mouse[0] < self.width + self.x_start and \
                self.y_start < mouse[1] < self.height + self.y_start:
            pygame.draw.rect(screen, self.color, (self.x_start, self.y_start,
                                                  self.width, self.height), 0)
            if click[0] == 1:
                button_sound.play()
                pressed = True
            if self.time < self.timer and pressed:
                c += self.a
                if c >= 255:
                    but_v = False
        else:
            pygame.draw.rect(screen, self.color1, (self.x_start, self.y_start,
                                                   self.width, self.height), 0)
        screen.blit(text, (self.x_start + (self.width - text.get_width()) // 2,
                           self.y_start + (
                                   self.height - text.get_height()) // 2))

        font = pygame.font.SysFont('American Captain Cyrillic', 80)
        text = font.render("Выход", 1, (80, 80, 80,))
        if self.x_output < mouse[0] < self.width + self.x_output and \
                self.y_output < mouse[1] < self.height + self.y_output:
            pygame.draw.rect(screen, self.color,
                             (self.x_output, self.y_output, self.width,
                              self.height), 0)
            if click[0] == 1:
                button_sound.play()
                running = False
        else:
            pygame.draw.rect(screen, self.color1,
                             (self.x_output, self.y_output, self.width,
                              self.height), 0)
        screen.blit(text, (self.x_output + (
                self.width - text.get_width()) // 2, self.y_output + (
                self.height - text.get_height()) // 2))


# ----------------------------Background---------------------------------------


class Background:
    def __init__(self):
        self.time = 0
        self.timer = 68
        self.a = 12
        self.pressed = pressed

    def render(self):
        global c, bg
        bg = pygame.image.load("data/images/background_game.png")
        c -= self.a
        self.time += 1


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/images/arrow.png")
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x, self.rect.y = pygame.mouse.get_pos()


# -----------------------------Main--------------------------------------------


def main():
    global running, width, height, button_sound, take_ground, give_ground, \
        stay_on_ground
    pygame.init()
    button_sound = pygame.mixer.Sound("data/music/button_sound.wav")
    take_ground = pygame.mixer.Sound("data/music/take_ground.wav")
    give_ground = pygame.mixer.Sound("data/music/give_ground.wav")
    stay_on_ground = pygame.mixer.Sound("data/music/stay_on_ground.wav")
    pygame.mixer.music.load("data/music/bg_music.mp3")
    pygame.mixer.music.play(-1)
    buttons = Buttons()
    phone = Background()
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    mouse = pygame.sprite.Group()
    person = pygame.sprite.Group()
    menu = pygame.sprite.Group()
    terrain = Terrain()
    person.add(Person())
    mouse.add(Mouse())
    menu.add(Menu())
    pygame.mouse.set_visible(False)
    while running:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
                break
        screen.fill((249, 226, 15))
        screen.blit(bg, (bx, by))
        if but_v:
            buttons.render(screen)
            font_name = pygame.font.SysFont('American Captain Cyrillic', 200)
            text_name = font_name.render(f"Fake Life", 1, (16,166,109))
            screen.blit(text_name, ((width - 600) // 2, height - 200))
        else:
            if c > 0:
                phone.render()
            terrain.render(screen)
            terrain.update()
            person.draw(screen)
            person.update(screen)
            menu.draw(screen)
            menu.update()
            font = pygame.font.SysFont('American Captain Cyrillic', 80)
            text = font.render(f"Блоки: {invent}", 1, (80, 80, 80))
            screen.blit(text, (50, 50))
        pygame.draw.rect(surf_alpha, (0, 0, 0), (0, 0, width, height))
        surf_alpha.set_alpha(c)
        screen.blit(surf_alpha, (0, 0))
        mouse.draw(screen)
        mouse.update()
        pygame.display.flip()
        clock = pygame.time.Clock()
        clock.tick(fps)
    pygame.quit()


if __name__ == '__main__':
    main()
