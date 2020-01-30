import pygame
import random

pygame.init()

#set up window and header
screen = pygame.display.set_mode((800,500))
pygame.display.set_caption('Fence Run')

#loading in all images
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]

obstacles = pygame.image.load('obstacle2.png')

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumpCount = 10
        self.isJump = False
        self.walkCount = 0
        self.hitbox = (self.x + 30, self.y +33, self.width - 65, self.height - 40)
        self.hit = False
        
    def draw(self, screen):
        if self.walkCount + 1 > 9:
            self.walkCount = 0
        if self.walkCount <= 9:
            screen.blit(pygame.transform.scale(walkRight[self.walkCount], (self.width,self.height)), (int(self.x),int(self.y)))
            if P1.hit != True and P1.y == 300:
                self.walkCount +=1
            
        self.hitbox = (self.x + 30, self.y +33, self.width - 65, self.height - 40)
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
    
    def jump(self):
        if P1.isJump == True:
            if P1.jumpCount > 0:
                P1.y -= (P1.jumpCount ** 2) // 2.5 * 1
                P1.jumpCount -= 1

            if P1.jumpCount == 0:
                P1.jumpCount -= 1

            if P1.jumpCount < 0 and P1.jumpCount > -12:
                P1.y -= (P1.jumpCount ** 2) // 2.5 * -1
                P1.jumpCount -= 1

            if P1.jumpCount == -11:
                P1.jumpCount = 10
                P1.isJump = False
             
class background(object):
    def __init__(self, speed, image, width, height):
        self.background = pygame.image.load(image)
        self.background2 = pygame.image.load(image)
        
        self.background = pygame.transform.scale(self.background, (width,height))
        self.background2 = pygame.transform.scale(self.background2, (width,height))
        
        self.scrollSpeed = speed
        self.x = 800
        
    def drawBackground(self, screen):
        
        screen.blit(self.background2, (0,0), (800 - self.x, 0, self.x, 500))
        screen.blit(self.background, (0 + self.x,0), (0, 0, 800 - self.x , 500))
        
        if P1.hit != True:
            if self.x - self.scrollSpeed > 0:
                self.x -= self.scrollSpeed
            else:
                self.x = 800
                
    def reset(self):
        self.x = 800
            
class obstacle(object):
    def __init__(self, x, y, width, height, difficulty):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.obstacleNumber = difficulty
        self.obstacle = obstacles
        self.scrollSpeed = 10
        self.hitbox = (x,y,width,height)
        self.maxScore = 1
        self.score = 0
        self.counter = 1
        
    def drawObstacle(self, screen):
        self.hitbox = (self.x,self.y,self.width,self.height)
        #pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)
        screen.blit(pygame.transform.scale(self.obstacle, (self.width,self.height)), (int(self.x),int(self.y)))
        
        if P1.hit != True:
            if self.x - self.scrollSpeed > 0:
                self.x -= self.scrollSpeed
            else:
                self.x = 800
                self.height = random.randint(60,115)
                self.y = 435 - self.height
                
                self.counter += 1
                
            if self.x + self.width < P1.x:
                self.maxScore = self.counter
                if self.score < self.maxScore:
                    self.score += 1
                
    def reset(self):
        self.x = 800
        self.maxScore = 1
        self.score = 0
        self.counter = 1

class button(object):
    def __init__(self, x, y, width, height, color, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
    
    def drawButton(self, surface, outline):
        if outline:
            pygame.draw.rect(surface, (0,0,0), (self.x - 2, self.y - 2, self.width + 4, self.height+4),0)
        
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != "":
            font = pygame.font.SysFont('comicsans', 20, True)
            text = font.render("Click to play again", 1, (0,0,0))
            screen.blit(text, (self.x + int(self.width/2 - text.get_width()/2), self.y + int(self.height/2 - text.get_height()/2)))
        
    def mouseCheck(self):
        if pos[0] > self.x and pos[0] < self.width + self.x:
            if pos[1] > self.y and pos[1] < self.height + self.y:
                return True
        
        return False

def redrawGame():
    if P1.hit != True:
        text = font.render('Score: ' + str(ob.score), 1, (0,125,125))
        bg.drawBackground(screen)
        screen.blit(text, (660, 10))
        P1.draw(screen)
        P1.jump()
        ob.drawObstacle(screen)
        
        pygame.display.update()
           
    else: # P1.hit == True:
        end = endFont.render("Your score was: "+ str(ob.score), 1, (0,125,125))
        bg.drawBackground(screen)
        P1.draw(screen)
        ob.drawObstacle(screen)
        screen.blit(end, (240, 200))
        text = font.render('', 1, (0,0,0))
        screen.blit(text, (0,0))
        endButton.drawButton(screen, True)
        
        pygame.display.update()
  
#main loop
P1 = player(300, 300, 100, 140)
bg = background(10, 'full-bg.png', 800, 500)
ob = obstacle(700, 325, 40, 110, 1)
endButton = button(325, 50, 150, 75, (0, 125, 0), "Click to play again")

score = 0
font = pygame.font.SysFont('comicsans', 35, True)
endFont = pygame.font.SysFont('comicsans',50, True)


clock = pygame.time.Clock()
run = True
while run:
    clock.tick(30)
    
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        
        if event.type == pygame.QUIT:
            run = False
        
        if P1.hit == True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if endButton.mouseCheck():
                    P1.hit = False
                    bg.reset()
                    ob.reset()
                    redrawGame()
            
            if event.type == pygame.MOUSEMOTION:
                if endButton.mouseCheck():
                    endButton.color = (0, 125, 0)
                else:
                    endButton.color = (255, 0, 0)
        
    
    # collision check
    if P1.hitbox[1] + P1.hitbox[3] > ob.hitbox[1]:
        if (P1.hitbox[0] + P1.hitbox[2] < (ob.hitbox[0]+ob.hitbox[2]) and P1.hitbox[0] +  P1.hitbox[2] > ob.hitbox[0]):
            P1.hit = True

        if (P1.hitbox[0] < (ob.hitbox[0] + ob.hitbox[2]) and P1.hitbox[0] > ob.hitbox[0]):
            P1.hit = True
    
    #check to add score
    if P1.hitbox[0] > ob.hitbox[0] + ob.hitbox[2]:
        if ob.score < ob.maxScore:
            ob.score += 1
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        P1.isJump = True
        P1.walkCount = 0
    
    redrawGame()

pygame.quit()