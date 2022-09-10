'''Game_Live'''

from pygame import init
import pygame
import copy
import math
import random

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win,outline,(self.x-2,self.y-2,self.width+4,self.height+4),0)
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height),0)
        if self.text!= '':
            font = pygame.font.SysFont('areal',self.width-70)
            text = font.render(self.text,1,(0,0,0))
            win.blit(text, (self.x+(self.width/2 - text.get_width()/2),self.y + (self.height/2 - text.get_height()/2)))
    def isOver(self,pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

class game_life():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Game_Life')
        self.screen = pygame.display.set_mode((500, 700))
        self.data = [[0 for j in range(50)] for i in range(50)]
        self.run = True
        self.clock = pygame.time.Clock()
        self.start = False
        self.initial = True
        self.resetButton = button((255,255,255),100,560,100,100,'Очистка')
        self.startButton = button((255,255,255),200,560,100,100,'Старт')
        self.randomButton = button((255, 255, 255), 300, 560, 100, 100, 'Случайно')

    def getData(self):
        return self.data
    def get_neighbour(self, i, j):
        neighbour = [[i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1], [i + 1, j + 1], [i - 1, j + 1], [i + 1, j - 1],
                     [i - 1, j - 1]]
        neighbour = [i for i in neighbour if 0 <= i[0] < 50 and 0 <= i[1] < 50]
        return neighbour

    def next_generation(self):
        self.last_generation = copy.deepcopy(self.data)
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                self.count = [self.last_generation[k[0]][k[1]] for k in self.get_neighbour(i, j)].count(1)
                if self.last_generation[i][j] == 1:
                    self.data[i][j] = 1 if self.count in range(2, 4) else 0
                elif self.last_generation[i][j] == 0:
                    self.data[i][j] = 1 if self.count == 3 else 0

    def update(self):
        self.screen.fill((255, 255, 255))
        self.resetButton.draw(self.screen, (0, 0, 0))
        self.startButton.draw(self.screen,(0, 0, 0))
        self.randomButton.draw(self.screen,(0, 0, 0))
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), (j * 10, i * 10, 10, 10))

    def user_initial(self):
        if self.initial:
                x, y = pygame.mouse.get_pos()
                if y < 500:
                    if pygame.mouse.get_pressed()[0]:
                        self.data[math.floor(y / 10)][math.floor(x / 10)] = 1
                    if pygame.mouse.get_pressed()[2]:
                        self.data[math.floor(y / 10)][math.floor(x / 10)] = 0
                self.clock.tick(60)
    def start_game(self):
        while self.run:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.resetButton.isOver(pos):
                        self.data = [[0 for j in range(50)] for i in range(50)]
                        self.start = False
                        self.initial = True
                    if self.startButton.isOver(pos):
                        if self.start:
                            self.start = False
                            self.initial = True
                        else:
                            self.start=True
                            self.initial=False
                    if self.randomButton.isOver(pos):
                        for i in range(len(self.data)):
                            for j in range(len(self.data[i])):
                                self.data[i][j]=random.randint(0,1)
                if event.type == pygame.QUIT:
                    self.run = False
            self.update()
            self.user_initial()
            if self.start:
                self.next_generation()
                self.clock.tick(10)
            pygame.display.update()

if __name__ == '__main__':
    game = game_life()
    game.start_game()
