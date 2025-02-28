import random
from time import sleep
import pygame
import os

class CarRacing:
    def __init__(self):
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        self.highscores = self.load_highscores()
        self.initialize()

    def initialize(self):
        self.crashed = False

        self.carImg = pygame.image.load('.\\img\\car.png')
        self.car_x_coordinate = (self.display_width * 0.45)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49

        # enemy_car
        self.enemy_car = pygame.image.load('.\\img\\enemy_car_1.png')
        self.enemy_car_startx = random.randrange(310, 450)
        self.enemy_car_starty = -600
        self.enemy_car_speed = 5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        # Background
        self.bgImg = pygame.image.load(".\\img\\back_ground.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def racing_window(self):
        pygame.display.set_caption('Car Dodge')
        self.run_car()

    def run_car(self):
        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_LEFT):
                        self.car_x_coordinate -= 50
                        print("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    if (event.key == pygame.K_RIGHT):
                        self.car_x_coordinate += 50
                        print("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    print("x: {x}, y: {y}".format(x=self.car_x_coordinate, y=self.car_y_coordinate))

            self.gameDisplay.fill(self.black)
            self.back_ground_raod()

            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.randrange(310, 450)

            self.car(self.car_x_coordinate, self.car_y_coordinate)
            self.highscore(self.count)
            self.count += 1
            if (self.count % 100 == 0):
                self.enemy_car_speed += 1
                self.bg_speed += 1
            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.car_x_coordinate > self.enemy_car_startx and self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width or self.car_x_coordinate + self.car_width > self.enemy_car_startx and self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = True
                    self.display_message("Game Over !!!")

            if self.car_x_coordinate < 310 or self.car_x_coordinate > 460:
                self.crashed = True
                self.display_message("Game Over !!!")

            pygame.display.update()
            self.clock.tick(60)

    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        self.display_credit()
        pygame.display.update()
        self.clock.tick(60)
        sleep(1)
        self.save_highscore(self.count)
        self.main_menu()

    def back_ground_raod(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def highscore(self, count):
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Score : " + str(count), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        text = font.render("Thanks for playing!", True, self.white)
        self.gameDisplay.blit(text, (600, 520))

    def main_menu(self):
        self.gameDisplay.fill(self.white)
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render("SHASHKI MANE", True, self.black)
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 100))

        button_width = 200
        button_height = 50
        button_margin = 20
        start_button = pygame.Rect(300, 250, button_width, button_height)
        instruction_button = pygame.Rect(300, 250 + button_height + button_margin, button_width, button_height)
        statistics_button = pygame.Rect(300, 250 + 2 * (button_height + button_margin), button_width, button_height)
        quit_button = pygame.Rect(300, 250 + 3 * (button_height + button_margin), button_width, button_height)

        pygame.draw.rect(self.gameDisplay, self.black, start_button)
        pygame.draw.rect(self.gameDisplay, self.black, instruction_button)
        pygame.draw.rect(self.gameDisplay, self.black, statistics_button)
        pygame.draw.rect(self.gameDisplay, self.black, quit_button)

        font = pygame.font.SysFont("comicsansms", 24, True)
        text = font.render("СТАРТ", True, self.white)
        self.gameDisplay.blit(text, (start_button.x + 50, start_button.y + 10))
        text = font.render("ИНСТРУКЦИЯ", True, self.white)
        self.gameDisplay.blit(text, (instruction_button.x + 20, instruction_button.y + 10))
        text = font.render("СТАТИСТИКА", True, self.white)
        self.gameDisplay.blit(text, (statistics_button.x + 20, statistics_button.y + 10))
        text = font.render("ВЫЙТИ", True, self.white)
        self.gameDisplay.blit(text, (quit_button.x + 50, quit_button.y + 10))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if start_button.collidepoint(mouse_pos):
                        self.initialize()
                        self.racing_window()
                    elif instruction_button.collidepoint(mouse_pos):
                        self.instruction_menu()
                    elif statistics_button.collidepoint(mouse_pos):
                        self.statistics_menu()
                    elif quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        quit()

    def instruction_menu(self):
        self.gameDisplay.fill(self.white)
        font = pygame.font.SysFont("comicsansms", 30, True)
        text = font.render("SHASHKI MANE - игра, суть которой", True, self.black)
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 200))
        text = font.render("не врезаться в автомобили в потоке", True, self.black)
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 250))
        text = font.render("Управляйте с помощью стрелочек на клавиатуре", True, self.black)
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 300))
        text = font.render("и зарабатывайте очки", True, self.black)
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 350))

        back_button = pygame.Rect(300, 450, 200, 50)
        pygame.draw.rect(self.gameDisplay, self.black, back_button)
        text = font.render("НАЗАД", True, self.white)
        self.gameDisplay.blit(text, (back_button.x + 50, back_button.y + 10))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if back_button.collidepoint(mouse_pos):
                        self.main_menu()

    def statistics_menu(self):
        self.gameDisplay.fill(self.white)
        font = pygame.font.SysFont("comicsansms", 36, True)
        text = font.render("Топ 5 рекордов:", True, self.black)
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 100))

        for i, score in enumerate(self.highscores[:5]):
            text = font.render(f"{i + 1}. {score}", True, self.black)
            self.gameDisplay.blit(text, (400 - text.get_width() // 2, 150 + i * 50))

        back_button = pygame.Rect(300, 450, 200, 50)
        pygame.draw.rect(self.gameDisplay, self.black, back_button)
        text = font.render("НАЗАД", True, self.white)
        self.gameDisplay.blit(text, (back_button.x + 50, back_button.y + 10))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if back_button.collidepoint(mouse_pos):
                        self.main_menu()

    def save_highscore(self, score):
        self.highscores.append(score)
        self.highscores.sort(reverse=True)
        with open("highscores.txt", "w") as file:
            for score in self.highscores[:5]:
                file.write(f"{score}\n")

    def load_highscores(self):
        if not os.path.exists("highscores.txt"):
            return []
        with open("highscores.txt", "r") as file:
            return [int(line.strip()) for line in file.readlines()]

if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.main_menu()