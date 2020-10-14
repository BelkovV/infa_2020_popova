import pygame
from pygame.draw import *
from time import ctime
from random import randint
import heart
clock = pygame.time.Clock()

pygame.init()

#GLOBAL constants
WIDTH = 1200
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
END_LINE = 'Please enter your name.'

RNG = 0 #If 1, varying marks will appear on special targets

#game files
PATH_LIST = 'score_list.txt'
PATH_MAIN = 'score_table.txt'
PATH_ORIG = '.scoredata.txt'

FPS = 20 #frames per second
K = 1.5 #number of balls appearing per second
W_T = 30 #time between creating white balls, seconds

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
ball_speed_max  = 300 #px/second
r_min = 20
r_max = 90
ball_lifetime = 10 #in seconds
white_ball_lifetime = 8 #in seconds
ball_points = 1
white_ball_points = 5

#GLOBAL variables
finished = False
balls = []
white_balls = []
timer = 0  
ball_score = 0
max_score = 0  #potential score if all the balls that disappeared were hit by player. Used in percentage calculations


#ball creation
def new_ball():
	x = randint(100, WIDTH-200)
	y = randint(100, HEIGHT-200)
	r = randint(r_min, r_max)
	dx = randint(-ball_speed_max, ball_speed_max)
	dy = randint(-ball_speed_max, ball_speed_max)
	i = randint(0, 5)
	color = COLORS[i]
	return [x, y, r, color, dx, dy, FPS*ball_lifetime, False]


def new_white_ball(do_random = 0):
	x = randint(100, WIDTH-200)
	y = randint(100, HEIGHT-200)
	dx = randint(-ball_speed_max, ball_speed_max)
	dy = randint(-ball_speed_max, ball_speed_max)
	r = randint(r_min, r_max)
	n = do_random*randint(0, 2)
	return [x, y, r, WHITE, dx, dy, FPS*white_ball_lifetime, False, r, n]


def move_ball(ball): # basic game logic
	ball[0] += ball[4]/FPS
	ball[1] += ball[5]/FPS
	# conditions of reflection from the walls
	if (ball[0] + ball[2] > WIDTH) or (ball[0] - ball[2] < 0):
		ball[4] *= -1
	if (ball[1] + ball[2] > HEIGHT) or (ball[1] - ball[2] < 0):
		ball[5] *= -1

	# countdown before death
	if not ball[7] and ball[6] >= 0:
		circle(screen, ball[3], (int(ball[0]), int(ball[1])), int(ball[2])) # ball draws itself
		ball[6]-=1

	# conditions for disappearing by natural causes
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
		
def scoreline(state, is_hidden): #converting data for scoreboards
	if is_hidden:
		res = ''
		for var in state:
			res += (var+' % ')
		return res[:-3] + '\n'
	return state[0] + ' played the game at ' + state[1] + ' and scored ' + state[2] + ' points in ' + state[3] + ' seconds (' + state[4] + ' percents)\n'

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
					ball_score += ball_points*a
					ball[7] = True
				ball_score += think(event, ball)
			for white_ball in white_balls:
				a = think(event, white_ball)
				if a>0:
					ball_score += white_ball_points*a
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
			max_score += ball_points
			continue
		i+=1

	# processing special white balls
	i = 0
	while i < len(white_balls):
		white_ball = white_balls[i]
		white_ball = move_ball(white_ball) #drawing, movement
		
		#radius decrease
		white_ball[2] -= white_ball[8]/(FPS*white_ball_lifetime)
		
		if white_ball[2] <= 0:
			white_ball[7] = True

		if white_ball[7] == True:
			white_balls.pop(i) #ball dies
			max_score += white_ball_points
			continue

		x = white_ball[0]
		y = white_ball[1]
		r = white_ball[2]
		
		if white_ball[9] == 0:
			polygon(screen, SPECIAL_RED, [(int(x), int(y-r/2)), (int(x+r/2), int(y)), (int(x), int(y+r/2)), (int(x-r/2), int(y))]) #diamonds mark, default
		elif white_ball[9] == 1:
			heart.heart(screen, SPECIAL_RED, x, y-int(r*(-0.5 + 2**0.5)/6), r/2) #hearts mark
		else:
			centre = y+int(r*(-0.5 + 2**0.5)/6)
			heart.heart(screen, BLACK, x, centre, -r/2)
			polygon(screen, BLACK, [(x, centre + r//12), (int(x - r/6), centre + r*(3**0.5)/6 + r//12), (int(x + r/6), centre + r*(3**0.5)/6 + r//12)]) #black mark
		i+=1

	# creating new balls
	if timer % (FPS//K) == 0:
		balls.append(new_ball())
	
	# creating white balls
	if timer % (W_T*FPS) == 0:
		white_balls.append(new_white_ball(RNG))
	   
	timer += 1  # game time count
	pygame.display.update()
	clock.tick(FPS)
	screen.fill(BLACK)  # updating the display

if max_score > 0:
	score = 100*(ball_score/max_score)
else:
	score = 0.0	
	
pygame.quit()

print(END_LINE)

#name reading & fool proof
name = input()
name = name.split(' % ')
true_name = ''
for elem in name:
	true_name+=elem
	true_name+=' '
name = true_name[:-1]

if name!='none':
	#score writing
	gametime = ctime()
	gamestate = [name, gametime, str(ball_score), str(timer//FPS), str(score)]
	
	f_list = open(PATH_LIST, 'a')
	f_list.write(scoreline(gamestate, False))
	f_list.close()
	
	table = []
	written = False
	f_orig = open(PATH_ORIG, 'r')
	for line in f_orig:
		a = line[:-1].split(' % ')
		if not written and (score > float(a[-1]) or (score == float(a[-1]) and ball_score > int(a[2]))):
			table.append(gamestate)
			written = True
		table.append(a)
	f_orig.close()
	
	f_orig = open(PATH_ORIG, 'w')
	for a in table:
		f_orig.write(scoreline(a, True))
	f_orig.close()

	f_main = open(PATH_MAIN, 'w')
	for a in table:
		f_main.write(scoreline(a, False))
	f_main.close()



