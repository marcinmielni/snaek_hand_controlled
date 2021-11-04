import pygame
import random
from Obj.objects import Snake, Food
import Obj.HandTrackingModule as htm
import cv2
import time
import sys


BACKGROUND_COLOR = (0, 0, 0)        #color theme
WHITE = (255, 255, 255)
BLUE = (0, 0, 200)


def msg(surface, str, x, y, fontSize = 64):
    pygame.font.init()
    font = pygame.font.SysFont(None, fontSize)
    text = font.render(str, True, WHITE, BACKGROUND_COLOR)
    textRect = text.get_rect()
    textRect.center = (x, y)
    surface.blit(text, textRect)
    pygame.font.quit()

def trimDirection(direction, value):
    def sign(x):
        if x == 0:
            return 0
        else:
            return x/abs(x)
    if abs(direction[0]) > abs(direction[1]):
        return (value * sign(direction[0]), 0)
    else:
        return (0, value * -(sign(direction[1])))

def main(size = 100, resolution = 1000):                            #adjust number of grid in window, and resolution
    pygame.init()

    cubeSize = resolution // size

    dis = pygame.display.set_mode((resolution, resolution))         # window opening
    pygame.display.set_caption('S N A E K')
    pygame.display.update()

    game_over = True
    game_close = False

    clock = pygame.time.Clock()
    clockTick = 15                                                  #adjust speed of the game, it will also affect hand detection

    cap = cv2.VideoCapture(0)

    pTime = 0
    cTime = 0
    detector = htm.handDetector(False, 1)
    
    while not game_close:                                               #game loop
        cv2.destroyAllWindows()
        msg(dis, "Press Enter to play", resolution//2, resolution//2, 64)
        msg(dis, "Press Esc to quit", resolution//2, 3 * resolution//4, 32)
        pygame.display.update()
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    game_over = True
                    game_close = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = False
                        snk = Snake(resolution // 2, resolution // 2, cubeSize)             #initializing snake
                        fd = Food(cubeSize, resolution)                                     #initializing food
                        direction = (0, 0)
        while not game_over:                                            #playing loop

            success, img = cap.read()                                   #initializing hand detection
            img = detector.findHands(img, False)
            lmList = detector.findPosition(img, 0 , False)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    game_over = True
                    game_close = True
                    sys.exit()
            if lmList:
                direction = trimDirection(detector.line(img, lmList, 5, 8), cubeSize)
                #if event.type == pygame.KEYDOWN:
                #    if event.key == pygame.K_LEFT:
                #        direction = (-cubeSize, 0)
                #    elif event.key == pygame.K_RIGHT:
                #        direction = (cubeSize, 0)
                #    elif event.key == pygame.K_UP:
                #        direction = (0, -cubeSize)
                #    elif event.key == pygame.K_DOWN:
                #        direction = (0, cubeSize)

            snk.Move(direction)
            #print(snk.segments)

            if snk.isCollision():
                game_over = True
            
            if snk.x >= resolution or snk.x < 0 or snk.y >= resolution or snk.y < 0:
                game_over = True

            if snk.x == fd.x and snk.y == fd.y:
                #clockTick += 1
                snk.Eat()
                fd.GetNew()
                clock.tick(clockTick)

                

            dis.fill(BACKGROUND_COLOR)
            snk.Draw(dis)
            fd.Draw(dis)
    
            clock.tick(clockTick)
            pygame.display.update()

            cTime = time.time()                                                             #calculating fps
            fps = 1/(cTime - pTime)
            pTime = cTime

            img = cv2.flip(img, 3)
            cv2.putText(img, str(int(fps)),(10,30), cv2.FONT_HERSHEY_PLAIN, 2, (100, 255, 0), 2)
            cv2.imshow("Image", img)
            cv2.waitKey(1)

        
        clock.tick(100)
    #pygame.display.quit()
    #pygame.quit()
    #sys.quit()
    return 0
    

main()