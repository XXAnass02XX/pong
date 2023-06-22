#!/usr/bin/env python3
import pygame
import random
import time
pygame.init()

WIDTH,HEIGHT = 800,800
PADDLE_WIDTH = WIDTH//100
PADDLE_HEIGHT = HEIGHT//7 #114
MAX_FPS = 60
WHITE =(255,255,255)
BLACK = (0,0,0)
Y_VEL_VAL = [-5+1*i for i in range(11)]
ball_radius = 15

window = pygame.display.set_mode((WIDTH,HEIGHT))
TEXT_FONT = pygame.font.SysFont("comicsansms",70)
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
    def move(self,up):
        '''move the paddle'''
        if up == True:
            if self.y -5>=0:
                self.y -= 5
        else:
            if self.y +5<=HEIGHT-PADDLE_HEIGHT:
                self.y +=5

class Ball:
    COLOR= WHITE

    def __init__(self,x,y,radius):
        self.x=x
        self.y=y
        self.radius = radius
        self.x_vel = 5
        self.y_vel = random.choice(Y_VEL_VAL)


    def draw(self,window):
        pygame.draw.circle(window,self.COLOR,(self.x,self.y),self.radius)

    def move(self,paddles):
        if ball_radius <= self.y + self.y_vel <= HEIGHT - ball_radius:
            self.y += self.y_vel
        elif self.y_vel<0:
            self.y = ball_radius
        else:
            self.y = HEIGHT-ball_radius
        if self.x_vel<0:
            if paddles[0].y <= self.y <= paddles[0].y + PADDLE_HEIGHT:
                if self.x + self.x_vel - ball_radius<= paddles[0].x+PADDLE_WIDTH:
                    self.x =paddles[0].x+PADDLE_WIDTH+ball_radius
                else:
                    self.x += self.x_vel
            else:
                self.x += self.x_vel
        if self.x_vel>0:
            if paddles[1].y <= self.y <= paddles[1].y + PADDLE_HEIGHT:
                if self.x + self.x_vel + ball_radius>= paddles[1].x:
                    self.x =paddles[1].x-ball_radius
                else:
                    self.x += self.x_vel
            else:
                self.x += self.x_vel

def handle_paddle_movement(keys,left_paddle,right_paddle):
    if keys[pygame.K_z]:
        left_paddle.move(up=True)
    if keys[pygame.K_s]:
        left_paddle.move(up=False)
    if keys[pygame.K_UP]:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN]:
        right_paddle.move(up=False)


def fill_window(window,paddles,ball,score1,score2):
    '''draw the image in the window'''
    window.fill(BLACK)
    left_score = TEXT_FONT.render(f"{score1}",1,WHITE)
    right_score = TEXT_FONT.render(f"{score2}",1,WHITE)
    window.blit(left_score,(WIDTH//4-left_score.get_width()//2,40))
    window.blit(right_score,(3*(WIDTH//4)-left_score.get_width()//2,40))
    for paddle in paddles:
        paddle.draw(window)
    ball.draw(window)
    pygame.display.update()

def update_y_vel_collision(ball_y,paddle_y):
    '''une bijection vers 11 elements'''
    for i in range(11):
        if (PADDLE_HEIGHT//11)*i-5 <=ball_y -paddle_y <= (PADDLE_HEIGHT//11)*(i+1)+5: #les +-5 to avoid a bug
            return Y_VEL_VAL[i]


def collision_ball_check(ball,paddles):
    '''check if the ball makes contact with an edge 
    and changes its direction'''
    if ball.y - ball.radius == 0:
        '''check if the ball hits the upper edge'''
        ball.y_vel = -ball.y_vel
    elif ball.y + ball.radius == HEIGHT:
        '''check if the ball hits the bottom edge'''
        ball.y_vel = -ball.y_vel
    '''check if the ball hits the right paddle'''
    if ball.x - ball_radius== paddles[0].x+PADDLE_WIDTH:
        if paddles[0].y <= ball.y <= paddles[0].y+PADDLE_HEIGHT:
            ball.x_vel = -ball.x_vel
            ball.y_vel = update_y_vel_collision(ball.y,paddles[0].y)
    elif ball.x + ball_radius== paddles[1].x:
        if paddles[1].y <= ball.y <= paddles[1].y+PADDLE_HEIGHT:
            ball.x_vel = -ball.x_vel
            ball.y_vel = update_y_vel_collision(ball.y,paddles[1].y)
    
def main():
    '''main fonc that displays the game window'''
    running= True
    score_1 = 0
    score_2 = 0
    while running:
        left_paddle = Paddle(5,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)
        right_paddle = Paddle(WIDTH-PADDLE_WIDTH-5,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)
        paddles = (left_paddle,right_paddle)
        ball = Ball(WIDTH//2,HEIGHT//2,ball_radius)
        ball.x_vel = ball.x_vel* random.choice([-1,1])
        fill_window(window,paddles,ball,score_1,score_2)
        time.sleep(1)
        while score_2 < 3 and score_1 < 3 and running != False:
            fill_window(window,paddles,ball,score_1,score_2)
            clock.tick(MAX_FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running= False
                    break
            keys = pygame.key.get_pressed()
            handle_paddle_movement(keys,left_paddle,right_paddle)
            collision_ball_check(ball,paddles)
            ball.move(paddles)
            if ball.x < 0:
                score_2 +=1
                if score_2 ==3:
                    winner = TEXT_FONT.render("the right player won",1,WHITE)
                    window.blit(winner,(WIDTH//2-winner.get_width()//2,400))
                    pygame.display.flip()
                    time.sleep(2)
                    running = False
                break
            elif ball.x > WIDTH:
                score_1+=1
                if score_1 ==3:
                    winner = TEXT_FONT.render("the left player won",1,WHITE)
                    window.blit(winner,(WIDTH//2-winner.get_width()//2,400))
                    pygame.display.flip()
                    time.sleep(2)
                    running = False
                break
    pygame.quit()

if __name__ == '__main__':
    main()
