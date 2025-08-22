from random import randint
import os
import pygame

beige = (238, 223, 176)
green = (74, 151, 18)
grey = (177, 185, 182)

width_area = 200
height_area = 40

pygame.init()
window_size = (600, 600)
pygame.display.set_caption("Поймай мячи")
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
background = pygame.image.load('pole.jpg')
background = pygame.transform.scale(background, (600, 600))


class Button:
    def __init__(self, x, y, width, height, color1, color2, text):
        self.button_txt = Text(x+20, y+10, text, color1)
        self.btn_input1 = Area(x, y, width, height, color1)
        self.btn_input2 = Area(x+5, y+5, width+-10, height-10, color2)
        self.rect = self.btn_input1.rect

    def draw_btn(self):
        self.btn_input1.draw()
        self.btn_input2.draw()
        self.button_txt.write()


class Area:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


class Text:
    def __init__(self, x, y, txt, color=green, size=30):
        self.font = pygame.font.Font(None, size)
        self.txt = txt
        self.text = self.font.render(self.txt, True, color)
        self.x = x
        self.y = y

    def write(self):
        screen.blit(self.text, (self.x, self.y))


class Goal:
    def __init__(self, x, y, width, height, image, speed, points):
        self.name = image
        image = pygame.image.load(image)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.points = points

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < 520:
            self.rect.x += self.speed

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def collision(self, f_group):
        obj = pygame.sprite.spritecollideany(self, f_group)
        if obj:
            if obj.name == 'bomb.png':
                obj.kill()
                return 'bomb'
            else:
                obj.kill()
                return self.points + 1
        else:
            return self.points


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, speed):
        super().__init__()
        self.name = image
        image = pygame.image.load(image)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 75:
            self.rect.y = 500
            self.rect.x = randint(15, 585)

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Table:
    def __init__(self, x, y, name, point, color=green):
        self.name = Text(x, y, name, color)
        self.points = Text(x+50, y, point, color)
        self.x = x
        self.y = y

    def draw_line(self):
        screen.blit(self.name.text, (self.x, self.y))
        screen.blit(self.name.text, (self.x, self.y))
        screen.blit(self.points.text, (self.x+200, self.y))


btn_back = Button(200, 400, width_area, height_area, green, beige, 'Назад в меню')
help_area = Area(100, 200, width_area*2, height_area, beige)
input_area = Area(200, 250, width_area, height_area, beige)
btn_start = Button(200, 300, width_area, height_area, green, beige, 'Начать игру')
btn_rules = Button(200, 350, width_area, height_area, green, beige, 'Правила игры')
back_rect = Area(0, 0, 600, 50, beige)
txt1 = Text(20, 200, 'В этой игре необходимо набрать больше 30 очков за 20 секунд.', size=23)
txt2 = Text(20, 260, 'Тарелкой можно управлять клавишами "вправо"/"влево".', size=23)
txt3 = Text(20, 230, 'Вы выиграете, если наберете 30 очков!', size=23)
txt4 = Text(20, 290, 'Но остерегайтесь бомб! Коснувшись бомбы, вы проиграете :(', size=23)
exp_group = []
names_bomb = os.listdir('Explosion')
for j in names_bomb:
    e = Ball(150, 75, 300, 300, 'Explosion/' + j, 0)
    exp_group.append(e)
plate = Goal(250, 75, 168, 93, 'goals.png', 9, 0)
