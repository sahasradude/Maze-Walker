#created by: Dhruva Sahasrabudhe
#MIS ID:     111408051
#Branch:     TY IT
#Year:       2016
#License:    Simplified BSD License

#MAZE WALKER

import pygame, sys, random, time
from pygame.locals import *
WINDOWX = 720#x and y coordinates of window
WINDOWY = 600
FPS = 30 #refresh rate of screen
TILEWIDTH = 50
TILEHEIGHT = 85
TILEFLOORHEIGHT = 45
#RGB values for colours
#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)
BGMAIN = NAVYBLUE
BGTEXT = YELLOW
BGHL = WHITE
def main():
    pygame.init()
    global sprite, clock, SCREEN, TILEDICT, titleFont, textFont, boySprite, pinkgirlSprite, catgirlSprite, horngirlSprite, blockSprite, grassSprite, rockSprite, SPRITEDICT, MAPWIDTH, MAPHEIGHT
    clock = pygame.time.Clock()
#fonts and sprites are loaded
    titleFont = pygame.font.Font('./fonts/AlexBrush-Regular.ttf', 50)
    textFont = pygame.font.Font('./fonts/CaviarDreams.ttf', 30)
    boySprite = pygame.image.load('./sprites/boy.png')
    pinkgirlSprite = pygame.image.load('./sprites/pinkgirl.png')
    catgirlSprite = pygame.image.load('./sprites/catgirl.png')
    horngirlSprite = pygame.image.load('./sprites/horngirl.png')
    grassSprite = pygame.image.load('./sprites/Grass_Block.png')
    blockSprite = pygame.image.load('./sprites/Plain_Block.png') 
    rockSprite = pygame.image.load('./sprites/Rock.png')
    wallSprite = pygame.image.load('./sprites/Wood_Block_Tall.png')
    goalSprite = pygame.image.load('./sprites/Selector.png')
    TILEDICT = {'#':wallSprite, ' ': blockSprite, '.': rockSprite, 'g': grassSprite, '$': goalSprite}
    SPRITEDICT = {'boy': boySprite, 'pinkgirl': pinkgirlSprite, 'catgirl': catgirlSprite, 'horngirl': horngirlSprite}
    
    difficulty, sprite = startup()
    level, MAPWIDTH, MAPHEIGHT = loadLevelFile(difficulty)
    pygame.mixer.music.load('./sounds/main.mp3')
    pygame.mixer.music.play(-1, 0.0)
    blockSound = pygame.mixer.Sound('./sounds/01blocked.wav')

    #focusCamera(level)
    keyPressed = False
    wongame = False
    drawscreen(level)
    while True:
        if keyPressed == True:
            drawscreen(level)
            keyPressed = False
        #getxy(playerRect)
        for event in pygame.event.get():            
            if event.type == KEYDOWN:    # Handle key presses
                if event.key == K_LEFT:
                    keyPressed = True
                    if validmove(level, 'left'):
                       level, wongame =  updatelevel(level, 'left')
                    else:
                    	blockSound.play()
                elif event.key == K_RIGHT:
                    keyPressed = True
                    if validmove(level, 'right'):
                       level, wongame = updatelevel(level, 'right')
                    else:
                    	blockSound.play()  
                elif event.key == K_UP:
                    keyPressed = True
                    if validmove(level, 'up'):
                        level, wongame = updatelevel(level, 'up')
                    else:
                    	blockSound.play()
                elif event.key == K_DOWN:
                    keyPressed = True
                    if validmove(level, 'down'):
                        level, wongame = updatelevel(level, 'down')
                    else:
                    	blockSound.play()
                else:
                	blockSound.play()

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()
        clock.tick(FPS)
        
        if wongame == True:
        	endAnim()  
        

def endAnim():

	wonSound = pygame.mixer.Sound('./sounds/correct.wav')
	wonSound.play()
	time.sleep(1)
	ENDSCREEN = pygame.display.set_mode((WINDOWX, WINDOWY))
	ENDSCREEN.fill(BGMAIN)
	endText = titleFont.render('Thank you for playing!', True, BGTEXT, BGMAIN)
	endRect = endText.get_rect()
	endRect.center = (int(WINDOWX/2), int(WINDOWY/4))    
	while True:
		ENDSCREEN.blit(endText, endRect)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update()
		clock.tick(FPS)
    
    
def updatelevel(level, direction):
    x, y = getplayerlocation(level)
    levtemp = []
    levelmod = []
    wongame = False
   
    
    for elem in level:
        levlist = list(elem)
        levtemp.append(levlist)
        
    if direction == 'left':
    	if levtemp[x - 1][y] == '$':
        	wongame = True
        	
    elif direction == 'right':
        if levtemp[x + 1][y] == '$':
        	wongame = True
        	
    elif direction == 'up':
        if levtemp[x][y - 1] =='$':
        	wongame = True
        	
    elif direction == 'down':
        if levtemp[x][y + 1] == '$':
        	wongame = True
    
    
    if direction == 'left':
        levtemp[x - 1][y] = '@'
        levtemp[x][y] = ' '
    elif direction == 'right':
        levtemp[x + 1][y] = '@'
        levtemp[x][y] = ' '
    elif direction == 'up':
        levtemp[x][y - 1] = '@'
        levtemp[x][y] = ' '
    elif direction == 'down':
        levtemp[x][y + 1] = '@'
        levtemp[x][y] = ' '
    
        	
    for elem in levtemp:
        levelmod.append(''.join(elem))
        
    return levelmod, wongame

    
def validmove(level, direction):
    x, y = getplayerlocation(level)
    if direction == 'left':
        if level[x - 1][y] == ' ' or  level[x - 1][y] == '$':
            return True
        else:
            return False
    if direction == 'right':
        if level[x + 1][y] == ' 'or  level[x + 1][y] == '$':
            return True
        else:
            return False
    if direction == 'up':
        if level[x][y - 1] == ' 'or  level[x][y - 1] == '$':
            return True
        else:
            return False
    if direction == 'down':
        if level[x][y + 1] == ' 'or  level[x][y + 1] == '$':
            return True
        else:
            return False
    
def loadLevelFile(difficulty):
    levelFile = open('./levels/' + difficulty + '.txt', 'r')
    l = levelFile.readlines()
    level = []
    
    for i in l:
        level.append(i.strip('\n'))
    width = len(level) * TILEWIDTH
    height = (len(level[0]) - 1)*TILEFLOORHEIGHT + TILEHEIGHT
    return level, width, height
    
def getplayerlocation(level):
    for x in range(len(level)):
        for y in range(len(level[x])):
            if level[x][y] == '@':
                return x, y

def drawscreen(level):			
    GAMESCREEN = pygame.display.set_mode((WINDOWX, WINDOWY))
    GAMESCREEN.fill(BGMAIN)
    playerpixx, playerpixy = getplayerlocation(level)
    playerx, playery = playerpixx * TILEWIDTH, playerpixy * TILEFLOORHEIGHT
    camx = 0
    camy = 0
    divx = int(MAPWIDTH/WINDOWX) + 1
    divy = int(MAPHEIGHT/WINDOWY) + 1
    paramx = int(MAPWIDTH/divx)
    paramy = int(MAPWIDTH/divy)
    totx = paramx
    toty = paramy
    while playerx > totx:
    	totx += paramx
    camx = totx - paramx
    while playery > toty:
    	toty += paramy
    camy = toty - paramy
    for x in range(len(level)):
        for y in range(len(level[x])):
            blockRect = pygame.Rect((x * TILEWIDTH - camx - 30, y * TILEFLOORHEIGHT - camy - 30, TILEWIDTH, TILEHEIGHT))
            tile = TILEDICT[' ']
            GAMESCREEN.blit(tile, blockRect)
            if level[x][y] in TILEDICT:
                tile = TILEDICT[level[x][y]]
                GAMESCREEN.blit(tile, blockRect)
            elif level[x][y] == '@':
                tile = SPRITEDICT[sprite]
                GAMESCREEN.blit(tile, blockRect)
                playerRect = blockRect
	
            


def startup(): #initial display screen
#title text
    STARTSCREEN = pygame.display.set_mode((WINDOWX, WINDOWY))
    STARTSCREEN.fill(BGMAIN)
    pygame.display.set_caption("Game")
    title = titleFont.render('Maze Walker', True, BGTEXT, BGMAIN)
    diffEasy = textFont.render('Easy', True, BGTEXT, BGMAIN)
    diffMed = textFont.render('Medium', True, BGTEXT, BGMAIN)
    diffHard = textFont.render('Hard', True, BGTEXT, BGMAIN)
    charSelect = textFont.render('Select Character', True, BGTEXT, BGMAIN)
    
    titleRect = title.get_rect()
    diffEasyRect = diffEasy.get_rect()
    diffMedRect = diffMed.get_rect()
    diffHardRect = diffHard.get_rect()
    charSelectRect = charSelect.get_rect()
    boySpriteRect = boySprite.get_rect()
    pinkgirlSpriteRect = pinkgirlSprite.get_rect()
    catgirlSpriteRect = catgirlSprite.get_rect()
    horngirlSpriteRect = horngirlSprite.get_rect()
    
    diffEasyRect.center = (int(WINDOWX/4), int(WINDOWY/2))
    diffMedRect.center = (int(WINDOWX/2), int(WINDOWY/2))
    diffHardRect.center = (int(3*WINDOWX/4), int(WINDOWY/2))
    charSelectRect.center = (int(WINDOWX/2), int(WINDOWY/4))
    boySpriteRect.center = (int(WINDOWX/5), int(3*WINDOWY/4))
    pinkgirlSpriteRect.center = (int(2*WINDOWX/5), int(3*WINDOWY/4))
    catgirlSpriteRect.center = (int(3*WINDOWX/5), int(3*WINDOWY/4))
    horngirlSpriteRect.center = (int(4*WINDOWX/5), int(3*WINDOWY/4))
    pygame.mixer.music.load('./sounds/intro.mp3')
    pygame.mixer.music.play(-1, 0.0)
    
    i = 0
    mousex = 0
    mousey = 0
    clicked = False
    
    while clicked != True:
        STARTSCREEN.fill(BGMAIN)
        if i <= int(WINDOWX/2):
            titleRect.center = (i, int(WINDOWY/4))
            i += 5
            STARTSCREEN.blit(title, titleRect) 
        else:
            STARTSCREEN.blit(title, titleRect) 
            STARTSCREEN.blit(diffEasy, diffEasyRect)
            STARTSCREEN.blit(diffMed, diffMedRect)
            STARTSCREEN.blit(diffHard, diffHardRect)
        #on mouse click 
        #event capture
        for event in pygame.event.get():
            if event.type == MOUSEMOTION :
                mousex, mousey = event.pos
                if diffEasyRect.collidepoint(mousex, mousey):
                    diffEasy = textFont.render('Easy', True, BGHL, BGMAIN)
                        
                elif diffMedRect.collidepoint(mousex, mousey):
                    diffMed = textFont.render('Medium', True, BGHL, BGMAIN)

                elif diffHardRect.collidepoint(mousex, mousey):
                    diffHard = textFont.render('Hard', True, BGHL, BGMAIN)
                else:
                    diffEasy = textFont.render('Easy', True, BGTEXT, BGMAIN)
                    diffMed = textFont.render('Medium', True, BGTEXT, BGMAIN)
                    diffHard = textFont.render('Hard', True, BGTEXT, BGMAIN)

            elif event.type == MOUSEBUTTONUP :
                mousex, mousey = event.pos
                if diffEasyRect.collidepoint(mousex, mousey):
                    difficulty = 'easy'
                    clicked = True
                        
                elif diffMedRect.collidepoint(mousex, mousey):
                    difficulty = 'medium'
                    clicked = True

                elif diffHardRect.collidepoint(mousex, mousey):
                    difficulty = 'hard'
                    clicked = True

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
        #update screen and tick clock    
        pygame.display.update()
        clock.tick(FPS)
    while True:
        STARTSCREEN.fill(BGMAIN)
        STARTSCREEN.blit(charSelect, charSelectRect)
        STARTSCREEN.blit(boySprite, boySpriteRect)
        STARTSCREEN.blit(catgirlSprite, catgirlSpriteRect)
        STARTSCREEN.blit(horngirlSprite, horngirlSpriteRect)
        STARTSCREEN.blit(pinkgirlSprite, pinkgirlSpriteRect)
        
        for event in pygame.event.get():
            if event.type == MOUSEMOTION :
                mousex, mousey = event.pos

            elif event.type == MOUSEBUTTONUP :
                mousex, mousey = event.pos
                clicked = True
                if clicked == True:
                    if boySpriteRect.collidepoint(mousex, mousey):
                        pygame.mixer.music.stop()
                        return difficulty, 'boy'
                    elif pinkgirlSpriteRect.collidepoint(mousex, mousey):
                        pygame.mixer.music.stop()
                        return difficulty, 'pinkgirl'
                    elif horngirlSpriteRect.collidepoint(mousex, mousey):
                        pygame.mixer.music.stop()
                        return difficulty, 'horngirl'
                    elif catgirlSpriteRect.collidepoint(mousex, mousey):
                        pygame.mixer.music.stop()
                        return difficulty, 'catgirl'
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
        #update screen and tick clock    
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()

