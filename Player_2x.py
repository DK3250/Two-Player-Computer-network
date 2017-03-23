import pygame, sys, socket
import connection
pygame.init()

""" This demonstrates a two-player game to be played from two different PCs
    connected to a local network (LAN) or even via the Internet. The code
    requeres access to the module 'connection' for handling of generel server
    and client code.

    Data send between the two players must be 'string'-format.
"""
## --- NEXT 4 LINES MUST BE MODIFIED TO MATCH ACTUAL SITUATION --- ##
MY_SERVER_HOST = '192.168.1.18'
MY_SERVER_PORT = 9991
OTHER_HOST = '192.168.1.10'
OTHER_PORT = 9990
## --------------------------------------------------------------- ##

X = 600
Y = 400

screen = pygame.display.set_mode((X, Y))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Player():
    def __init__(self, pos):
        self.img = pygame.surface.Surface((20, 20))
        self.rect = self.img.get_rect(center = pos)

    def move(self, dir):
        if dir == 'up' and self.rect.top > 0:
            self.rect.centery -= 2
        if dir == 'down' and self.rect.bottom < Y:
            self.rect.centery += 2
        if dir == 'left' and self.rect.left > 0:
            self.rect.centerx -= 2
        if dir == 'right' and self.rect.right < X:
            self.rect.centerx += 2

    def draw(self):
        screen.blit(self.img, self.rect)

    def makeDataPackage(self):
        datax = str(self.rect.centerx).rjust(4, '0')
        datay = str(self.rect.centery).rjust(4, '0')
        return datax + datay

class Player_1(Player):
    def __init__(self, pos=(100, 200)):
        super().__init__(pos)
        self.img.fill(RED)

class Player_2(Player):
    def __init__(self, pos=(300, 200)):
        super().__init__(pos)
        self.img.fill(BLUE)

## --- NEXT TWO LINES DEFINES PLAYER 1 AND 2 --- ##
me = Player_1()
enemy = Player_2()

## --- CREATION OF SERVER INSTANCE --- ##
server = connection.Server(MY_SERVER_HOST, MY_SERVER_PORT)        

## --- GAME LOOP ---  ##
while True:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server.shutdown()
            pygame.quit()
            sys.exit()

    ## --- GET INPUT FROM KEYBOARD --- ##
    keys = pygame.key.get_pressed()
    for button, direction in [(pygame.K_UP, 'up'), (pygame.K_DOWN, 'down'),
                              (pygame.K_LEFT, 'left'), (pygame.K_RIGHT, 'right')]:
        if keys[button]:
            me.move(direction)

    ## --- DATA TRANSFER --- ##
    me_data = me.makeDataPackage()
    connection.send(me_data, OTHER_HOST, OTHER_PORT) # the send code

    enemy_data = server.receive() # the receive code
    
    enemy.rect.centerx = int(enemy_data[:4])
    enemy.rect.centery = int(enemy_data[4:])

    ## --- UPDATE SCREEN --- ##
    enemy.draw()
    me.draw()
    pygame.display.flip()
    pygame.time.wait(50)
    
            
