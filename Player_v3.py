import pygame, sys, socket
import connection
pygame.init()

""" This demonstrates a two-player game to be played from two different PCs
    connected to a local network (LAN) or even via the Internet. The code
    requeres access to the module 'connection' for handling of generel server
    and client code.

    Data send between the two players must be 'string'-format.
"""

#####################################################################
## --- NEXT 4 LINES MUST BE MODIFIED TO MATCH ACTUAL SITUATION --- ##
MY_SERVER_HOST = '10.0.0.16'
MY_SERVER_PORT = 9999
OTHER_HOST = '192.168.1.18'
OTHER_PORT = 9992
#####################################################################

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

    def make_data_package(self):
        datax = str(self.rect.centerx).rjust(4, '0')
        datay = str(self.rect.centery).rjust(4, '0')
        return datax + datay


class Player_1(Player):
    def __init__(self, pos=(200, 200)):
        super().__init__(pos)
        self.img.fill(RED)


class Player_2(Player):
    def __init__(self, pos=(400, 200)):
        super().__init__(pos)
        self.img.fill(BLUE)


def ip_value(ip):
    """ ip_value returns ip-string as integer """
    return int(''.join([x.rjust(3, '0') for x in ip.split('.')]))


def define_players():
    if ip_value(MY_SERVER_HOST) > ip_value(OTHER_HOST):
        me = Player_1()
        enemy = Player_2()
    else:
        me = Player_2()
        enemy = Player_1()
    return me, enemy


def event_handling():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server.shutdown()
            pygame.quit()
            sys.exit()


def get_input():
    keys = pygame.key.get_pressed()
    for button, direction in [(pygame.K_UP, 'up'), (pygame.K_DOWN, 'down'),
                              (pygame.K_LEFT, 'left'), (pygame.K_RIGHT, 'right')]:
        if keys[button]:
            me.move(direction)


def data_transfer():
    me_data = me.make_data_package()
    connection.send(me_data, OTHER_HOST, OTHER_PORT) # the send code

    enemy_data = server.receive() # the receive code
    
    enemy.rect.centerx = int(enemy_data[:4])
    enemy.rect.centery = int(enemy_data[4:])


def update_screen():
    screen.fill(WHITE)
    enemy.draw()
    me.draw()
    pygame.display.flip()
    pygame.time.wait(50)


me, enemy = define_players()
server = connection.Server(MY_SERVER_HOST, MY_SERVER_PORT)        
            
while True:
    event_handling()
    get_input()
    data_transfer()
    update_screen()
