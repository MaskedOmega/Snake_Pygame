import pygame 
import time
import numpy as np

pygame.init()
pygame.display.set_caption("Snake Game")
font = pygame.font.Font('freesansbold.ttf', 26)

#change for game map size variations
GameSizeXY = [10,10]
#change for player speed variation lower values = faster movement default 0.5
playerSpeed = 0.5

ScreenSizeXY = [500,500]
Screen = pygame.display.set_mode(ScreenSizeXY)
scaleX = ScreenSizeXY[0] / GameSizeXY[0]
scaleY = ScreenSizeXY[1] / GameSizeXY[1]
screenCenterXY = ScreenSizeXY[0] / 2, ScreenSizeXY[1] / 2
map = np.zeros(GameSizeXY)

centerXY = [GameSizeXY[0] // 2, GameSizeXY[1] // 2]
playerX = [centerXY[0]]
playerY = [centerXY[1]]
playerLen = 1
playerFace = [-1,0]


def keypress(playerFace):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        playerFace = [0,-1]
        return(playerFace)
            
    if keys[pygame.K_s]:
        playerFace = [0,1]
        return(playerFace)

    if keys[pygame.K_a]:
        playerFace = [-1,0]
        return(playerFace)
            
    if keys[pygame.K_d]:
        playerFace = [1,0]
        return(playerFace)       
    
    return(playerFace) 

def pFowardVect(playerFace):
    Options = {-1, 1}

    if int(playerFace[0]) in Options:
        #print("changeX")
        Cords = [int(playerFace[0]), 0]
        playerX.append(playerX[-1] + Cords[0])
        playerY.append(playerY[-1] + Cords[1])

    if int(playerFace[1]) in Options:
        #print("changeY")
        Cords = [0, int(playerFace[1])]
        playerX.append(playerX[-1] + Cords[0])
        playerY.append(playerY[-1] + Cords[1])
    return(playerFace)

def playerEndDetec():
    endGame = False
    if playerX[-1] not in range(0,GameSizeXY[0]-1) or playerY[-1] not in range(0,GameSizeXY[1]-1):
        #print("hit wall")
        endGame = True
        return(endGame)
    

    zipped = list(zip(playerX, playerY))
    lastElemXY = zipped.pop()
    #print(zipped)
    if lastElemXY in zipped:
        #print("hitBody")
        endGame = True
        return(endGame)
    endGame = False
    return(endGame)

def drawOnMap(map):
    for i in range(np.size(map,0)):
        for j in range(np.size(map,1)):
            if int(map[i][j]) == 1:
                #[left, top, width, height]
                pygame.draw.rect(Screen,(255,0,0),(i*scaleX,j*scaleY,scaleX,scaleY),100,25)
            elif int(map[i][j]) == 2:
                pygame.draw.rect(Screen,(0,0,255),(i*scaleX,j*scaleY,scaleX,scaleY),100,15)
            if int(map[i][j]) == 0:
                #[left, top, width, height]
                pygame.draw.rect(Screen,(0,255,0),(i*scaleX,j*scaleY,scaleX,scaleY),1)

def updateObjects(map,removeXY):

    map[int(appleXY[0])][int(appleXY[1])] = 2

    if removeXY[0] != None:
        map[int(removeXY[0])][int(removeXY[1])] = 0

    for i in range(len(playerX)):
        map[int(playerX[i])][int(playerY[i])] = 1

def genApple(playerLen, playerX,playerY,appleXY):
    if playerX[-1] == appleXY[0]:
        if playerY[-1] == appleXY[1]:
            appleXY = np.random.randint(0,(GameSizeXY[0]-1)),np.random.randint(0,(GameSizeXY[1]-1))
            playerLen += 1
            #print("eat Apple")
            return(appleXY, playerLen)
    return(appleXY, playerLen)

removeX, removeY = None, None
appleXY = np.random.random_integers(0,(GameSizeXY[0]-1)),np.random.random_integers(0,(GameSizeXY[1]-1))

clock = pygame.time.Clock()
startTimeControls = time.time()

endGame = False

while True:
    Screen.fill((0,0,0))
    currentTime = time.time()
    
    if endGame == False:
        playerFace = keypress(playerFace)
        if (currentTime - startTimeControls) >= playerSpeed:
            startTimeControls = currentTime
            pFowardVect(playerFace)
        
        endGame = playerEndDetec()

        if len(playerX) > playerLen:
            removeX = playerX.pop(0)

        if len(playerY) > playerLen:
            removeY = playerY.pop(0)

        appleXY, playerLen = genApple(playerLen, playerX,playerY,appleXY)
        removeXY = [removeX,removeY]

        #print(playerX[-1],playerY[-1])
        updateObjects(map,removeXY)
        drawOnMap(map)

    if endGame == True:
        icon = pygame.draw.circle(Screen,(255,0,0),(screenCenterXY),15)
        text = font.render("Press R to restart", True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (250, 300)
        Screen.blit(text, textRect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            endGame = False
            playerX = [GameSizeXY[0] // 2]
            playerY = [GameSizeXY[1] // 2]
            playerLen = 1
            playerFace = [-1,0]
            map = np.zeros(GameSizeXY)
    
    pygame.display.update()
    clock.tick(60)
    if pygame.event.get() == pygame.QUIT:
        pygame.quit()
        break
