import pygame
import os

class GameState:
    def __init__(self):
        self.x = 120
        self.y = 120

    def update(self, moveCommandX, moveCommandY):
        self.x += moveCommandX
        self.y += moveCommandY

class UserInterface:
    def __init__(self) -> None:
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.display.set_caption("interesting game")

        self.window = pygame.display.set_mode((640,480))
        self.clock = pygame.time.Clock()
        self.gameState = GameState()
        self.running = True

        self.moveCommandX = 0
        self.moveCommandY = 0 

    def process_input(self):
        """ Handle User Input"""
        self.moveCommandX = 0
        self.moveCommandY = 0 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                    break
                elif event.key == pygame.K_RIGHT:
                    self.moveCommandX += 8
                elif event.key == pygame.K_LEFT:
                    self.moveCommandX -= 8
                elif event.key == pygame.K_DOWN:
                    self.moveCommandY += 8
                elif event.key == pygame.K_UP:
                    self.moveCommandY -= 8

    def update(self):
        """ Update Game State """
        self.gameState.update(self.moveCommandX, self.moveCommandY)

    def render(self):
        """ Render Game State """
        self.window.fill((0,0,0))
        pygame.draw.rect(self.window,(0,0,255),(self.gameState.x,self.gameState.y,400,240))
        pygame.display.update()

    def run(self):
        """ Main Loop """
        while self.running:
            self.process_input()
            self.update()
            self.render()
            self.clock.tick(60)