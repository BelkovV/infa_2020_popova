import pygame
from pygame.draw import *
from random import randint
clock = pygame.time.Clock()

pygame.init()

#GLOBAL constants
WIDTH = 1200
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#the number of frames per second
FPS = 20
#the number of balls appearing per second
K = 1.5 
#time between creating white balls
W_T = 50 

#lifetime of ordinary ball
ball_lifetime = 160 
#lifetime of white ball
white_ball_lifetime = 160 

#colors
RED = (255, 0, 0)
SPECIAL_RED = (180, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

#ball parameters
ball_speed_max  = 10
r_min = 40
r_max = 90

#GLOBAL variables
finished = False
balls = []
white_balls = []
timer = 0  
ball_score = 0
white_ball_score = 0


#ball creation
def new_ball():
	x = randint(100, WIDTH-200)
	y = randint(100, HEIGHT-200)
	r = randint(r_min, r_max)
	dx = randint(-ball_speed_max, ball_speed_max)
	dy = randint(-ball_speed_max, ball_speed_max)
	i = randint(0, 5)
	color = COLORS[i]
	return [x, y, r, color, dx, dy, ball_lifetime, False]


def new_white_ball():
	x = randint(100, WIDTH-200)
	y = randint(100, HEIGHT-200)
	dx = randint(-ball_speed_max, ball_speed_max)
	dy = randint(-ball_speed_max, ball_speed_max)
	r = randint(r_min, r_max)
	return [x, y, r, WHITE, dx, dy, white_ball_lifetime, False]


def move_ball(ball): # basic game logic
	ball[0] += ball[4]
	ball[1] += ball[5]
	# conditions of reflection from the walls
	if (ball[0] + ball[2] > WIDTH) or (ball[0] - ball[2] < 0):
		ball[4] *= -1
	if (ball[1] + ball[2] > HEIGHT) or (ball[1] - ball[2] < 0):
		ball[5] *= -1

	# countdown before death
	if not ball[7] and ball[6] >= 0:
		circle(screen, ball[3], (ball[0], ball[1]), ball[2])
		ball[6]-=1

	# condition for disappearing if the ball is old
	elif not ball[7]:
		ball[7] = True

	return ball


def think(event, ball): # conditions for hitting the ball
	(x_mouse, y_mouse) = event.pos
	if (not ball[7]) and ((ball[0] - x_mouse) ** 2 + (ball[1] - y_mouse) ** 2 <= ball[2] ** 2):
		ball[7] = True  # disappearance of the shot ball
		return 1
	else:
		return 0


pygame.display.update()


while not finished:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			#click processing
			for ball in balls:
				a = think(event, ball)
				if a>0:
					ball_score += a
					ball[7] = True
				ball_score += think(event, ball)
			for white_ball in white_balls:
				a = think(event, white_ball)
				if a>0:
					ball_score += 5*a
					white_ball[7] = True

	# score output on the game display
	f = pygame.font.Font(None, 64)
	text = f.render('Score: ' + str(ball_score), 1, SPECIAL_RED)
	screen.blit(text, (20, 20))

	# processing usual balls
	i = 0
	while i < len(balls):
		ball = balls[i]
		ball = move_ball(ball) #drawing, movement

		if ball[7] == True:
			balls.pop(i) #ball dies
			continue
		i+=1

	# processing special white balls
	i = 0
	while i < len(white_balls):
		white_ball = white_balls[i]
		white_ball = move_ball(white_ball) #drawing, movement

		white_ball[2] -= 1 #radius decrease
		if white_ball[2] <=0:
			white_ball[7] = True

		if white_ball[7] == True:
			white_balls.pop(i) #ball dies
			continue

		x = white_ball[0]
		y = white_ball[1]
		r = white_ball[2]
		polygon(screen, SPECIAL_RED, [(x, y-r//2), (x+r//2, y), (x, y+r//2), (x-r//2, y)]) #diamonds mark
		i+=1

	# creating new balls
	if timer % (FPS//K) == 0:
		balls.append(new_ball())
	
	# creating white balls
	if timer % (W_T) == 0:
		white_balls.append(new_white_ball())
	   

	timer += 1  # game time count
	pygame.display.update()
	clock.tick(FPS)
	screen.fill((0, 0, 0))  # updating the display

pygame.quit()
