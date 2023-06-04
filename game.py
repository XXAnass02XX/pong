#!/usr/bin/env python3
import pygame 
pygame.init()

WIDTH,HEIGHT = 800,800
PADDLE_WIDTH = WIDTH//20
PADDLE_HEIGHT = HEIGHT//7
MAX_FPS = 60
WHITE =(255,255,255)
BLACK = (0,0,0)

window = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("pong game")

class Paddle:
    COLOR = WHITE
    def __init__(self,x,y,width,height):
        '''the position and size of the paddle
        the x and y are the coordinates of the topleft
        of the rectangle'''
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def draw(self,window):
        '''draw the paddle'''
        pygame.draw.rect(window,self.COLOR,(self.x,self.y,self.width,self.height))
    def move(self,window):
        '''move the paddle'''
        pass

def fill_window(window,paddles):
    '''draw the image in the window'''
    window.fill(BLACK)
    for paddle in paddles:
        paddle.draw(window)
    pygame.display.update()

def main():
    '''main fonc that displays the game window'''
    running= True
    left_paddle = Paddle(5,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH-PADDLE_WIDTH-5,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)
    padles = (left_paddle,right_paddle)
    while running:
        fill_window(window,padles)
        clock.tick(MAX_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running= False
                break
    
    pygame.quit()

if __name__ == '__main__':
    main()
