import pygame
import random
import time
pygame.init()
display_width = 800
display_height = 600

crash_sound = pygame.mixer.Sound("Car_Screech_And_Crash.wav")
pygame.mixer.music.load("eminem-not_afraid.mp3")
#Define color definitios
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
red = (200,0,0)
bright_red = (255,0,0)
green = (0,200,0)
bright_green = (0,255,0)
block_color = (53,115,255)
car_width= 129
pause  = False

#Game screen bad practice to set dimensions therefore variables
gameDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('I am Speed')
#game clock
clock = pygame.time.Clock()
#Load image 
carImg = pygame.image.load('carss2.png')
caricon = pygame.image.load('caricon.png')
#Change icon of the game window
pygame.display.set_icon(caricon)

#Count score
def things_dodged(count):
	font = pygame.font.SysFont(None ,25)
	text = font.render("Dodged " + str(count), True , black)
	#to display over background
	gameDisplay.blit(text,(0,0))

def objects(objx,objy,objw,objh,color):
	 pygame.draw.rect(gameDisplay, block_color, [objx,objy,objw,objh])

def car(x,y):
	gameDisplay.blit(carImg,(x,y))

def text_objects(text,font):
	textSurface = font.render(text, True, blue)
	return textSurface, textSurface.get_rect()
def message_display(text):
	largeText = pygame.font.Font('freesansbold.ttf',100)
	TextSurf,TextRect = text_objects(text,largeText)
	TextRect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(TextSurf,TextRect)
	pygame.display.update()
	time.sleep(2)
	game_loop()
def crash():

	pygame.mixer.music.stop()
	pygame.mixer.Sound.play(crash_sound)

	largeText = pygame.font.Font('freesansbold.ttf',100)
	TextSurf,TextRect = text_objects('You Crashed',largeText)
	TextRect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(TextSurf,TextRect)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		
		button("Play Again",125,400,150,75,green,bright_green,game_loop)
		button("QUIT!",525,400,150,75,red,bright_red,quitgame)
		pygame.display.update()
		clock.tick(15)

def button(msg,x,y,w,h,ic,ac,action=None):
	#Get position of mouse
	mouse = pygame.mouse.get_pos()
	#Gets click in form of (0,0,0)
	click = pygame.mouse.get_pressed()
	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
		if click[0] == 1 and action!= None:
			#Action for button
			action()
	else:
		pygame.draw.rect(gameDisplay, ic, (x,y,w,h))

	smallText= pygame.font.Font("freesansbold.ttf",20)
	TextSurf,TextRect = text_objects(msg, smallText)
	TextRect.center = ((x+(w/2)), (y + h/2))
	gameDisplay.blit(TextSurf, TextRect)
def unpause():
	global pause
	pygame.mixer.music.unpause()
	pause = False


def paused():

	pygame.mixer.music.pause()

	largeText = pygame.font.Font('freesansbold.ttf',100)
	TextSurf,TextRect = text_objects('Paused',largeText)
	TextRect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(TextSurf,TextRect)

	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		
		button("Continue",125,400,150,75,green,bright_green,unpause)
		button("QUIT!",525,400,150,75,red,bright_red,quitgame)
		pygame.display.update()
		clock.tick(15)
def quitgame():
	pygame.quit()
	quit()	
def game_intro():

	intro  = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.fill(white)
		largeText = pygame.font.Font('freesansbold.ttf',100)
		TextSurf,TextRect = text_objects('Hi, I am Speed!',largeText)
		TextRect.center = ((display_width/2),(display_height/2))
		gameDisplay.blit(TextSurf,TextRect)

		button("GO!",125,400,150,75,green,bright_green,game_loop)
		button("QUIT!",525,400,150,75,red,bright_red,quitgame)
		pygame.display.update()
		clock.tick(15)
				
def game_loop():	
	global pause
	#play music indefinitely
	pygame.mixer.music.play(-1)
	x= (display_width * 0.45)
	y = (display_height* 0.78)
	x_change = 0
	#specifying obstacles
	thing_startx = random.randrange(0,display_width)
	thing_starty = -600
	thing_speed = 4
	thing_width = 100
	thing_height = 100

	dodged = 0
	gameExit = False
	while not gameExit:
	    #gets mouse and keyboards info
	    for event in pygame.event.get():
	        if event.type == pygame.QUIT:
	            pygame.QUIT()
	            quit()
	        #When key is pressed    
	        if event.type == pygame.KEYDOWN:
	        	if event.key == pygame.K_LEFT:
	        		x_change = -5
	        	if event.key == pygame.K_RIGHT:
	        		x_change = 5
	        	if event.key == pygame.K_SPACE:
	        		pause = True
	        		paused()	
	        #When key is released		
	        if event.type == pygame.KEYUP:
	        	if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
	        		x_change = 0		
	    x += x_change

	    #background        
	    gameDisplay.fill(white)

	    # objects(objx,objy,objw,objh,color)
	    objects(thing_startx,thing_starty, thing_width, thing_height, block_color)
	    #moving the object below
	    thing_starty += thing_speed
	    car(x,y)
	    things_dodged(dodged)
	    #To prevent car from going beyond screen(boundary)
	    if x > display_width - car_width or x < 0:
	    	crash()
	    	game_intro()
	    #bring object again	
	    if thing_starty > display_height:
	    	thing_starty = 0 - thing_height	
	    	thing_startx= random.randrange(0,display_width-thing_width)
	    	dodged += 1
	    	if thing_speed != 12:
	    		thing_speed += 0.5
	    	if thing_width != 200:	
	    		thing_width += 10	
	    #objects crashing car
	    if y < thing_starty+thing_height:
	    	if x > thing_startx and x < thing_startx+thing_width or x+car_width>thing_startx and x+car_width<thing_startx+thing_width:
	    		crash()
	    		game_intro()	

	    #to show everything in new screen after background processing    
	    pygame.display.update()
	    #fps
	    clock.tick(60)
game_intro()	    
game_loop()
pygame.quit()
quit()
 
