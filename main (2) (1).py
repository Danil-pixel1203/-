import pygame as pg
from math import sin, cos, pi
from random import randint, uniform
from pygame.math import Vector2


class Game:
    def __init__(self):
        pg.init()
        self.WIDTH = 700
        self.HEIGHT = 700
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption('Физика движения')
        self.bg_color = pg.Color('white')

        self.N_circles = 10 # количество шариков
        self.circle_list = self.generate_circles()

    def generate_circles(self):
        circles = list()
        for _ in range(self.N_circles):
            radius = randint(10, 20)
            vec = Vector2(x=randint(radius, self.WIDTH - radius),
                          y=randint(radius, self.HEIGHT - radius))
            speed = uniform(1, 8)
            angle = uniform(0, 2 * pi)
            circles.append(Circle(self, vec, radius, speed, angle))

        return circles

    def update(self):
        pg.time.Clock().tick(60)
        for circle in self.circle_list:
            circle.update()
        self.change_circle_list()
        pg.display.flip()

    def change_circle_list(self):
        left, _, right = pg.mouse.get_pressed(num_buttons=3)
        if left:
            radius = randint(10, 20)
            vec = Vector2(x=randint(radius, self.WIDTH - radius),
                          y=randint(radius, self.HEIGHT - radius))
            speed = uniform(1, 8)
            angle = uniform(0, 2 * pi)
            self.circle_list.append(
                Circle(self, vec, radius, speed, angle)
            )
        if right:
            if self.circle_list:
                self.circle_list.pop()

    def draw(self):
        self.screen.fill(self.bg_color)
        for circle in self.circle_list:
            circle.draw()

    @staticmethod
    def check_events():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
        return True

    def run(self):
        while self.check_events():
            self.update()
            self.draw()
        pg.quit()


class Circle:
    def __init__(self, root: Game, vec: Vector2, radius, speed, angle):
        self.game = root  # Поле нашего приложения
        self.vec = vec  # вектор центра
        self.radius = radius  # радиус шарика

        self.color = pg.Color('blue')  # цвет шара
        self.thickness = 3  # размер контура шарика
        self.speed = speed  # скорость движения шарика
        self.angle = angle  # угол направления шарика

    def draw(self):
        pg.draw.circle(self.game.screen, self.color, self.vec, self.radius, self.thickness)

    def move(self):
        self.vec.x += cos(self.angle) * self.speed
        self.vec.y -= sin(self.angle) * self.speed

    def bounce(self):
        w = self.game.WIDTH
        h = self.game.HEIGHT

        if self.vec.x > w - self.radius:
            self.angle = pi - self.angle

        if self.vec.x <= self.radius:
            self.angle = pi - self.angle

        if self.vec.y > h - self.radius:
            self.angle = -self.angle

        if self.vec.y <= self.radius:
            self.angle = -self.angle

    def update(self):
        self.move()
        self.bounce()


if __name__ == '__main__':
    game = Game()
    game.run()