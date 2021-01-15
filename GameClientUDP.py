import socket
import pygame


pygame.init()


width = 700
height = 500


screen = pygame.display.set_mode((width, height))


clock = pygame.time.Clock()


font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Waiting for the Other Player', True, (0, 255, 0), (0, 0, 255))
textRect = text.get_rect() 
textRect.center = (width // 2, height // 2) 

server_ip = '192.168.1.102'
server_port = 65432


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_socket.connect((server_ip, server_port))

two_players = False

class Player1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.speedx = 0
        self.speedy = 0
    
    def update(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -2
        if keystate[pygame.K_RIGHT]:
            self.speedx = 2
        if keystate[pygame.K_UP]:
            self.speedy = -2
        if keystate[pygame.K_DOWN]:
            self.speedy = 2
        
        self.rect.x = self.rect.x + self.speedx
        self.rect.y = self.rect.y + self.speedy

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.left = width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.left = height

player1 = Player1()
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)

class Player2(pygame.sprite.Sprite):
    global two_players
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()

        self.two_players = False
    
    def update(self):
        player1_position = str(player1.rect.x) + ',' + str(player1.rect.y)
        server_socket.sendto(player1_position.encode('utf-8'), (server_ip, server_port))

        player2_position = server_socket.recvfrom(1024)[0].decode('utf-8')

        self.rect.x = int(player2_position.split(',')[0])
        self.rect.y = int(player2_position.split(',')[1])
        # print(self.rect.x)
        # print(two_players)

        if self.rect.x >= 0:
            self.two_players = True
            # print(two_players)


player2 = Player2()
all_sprites.add(player2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            break
    
    all_sprites.update()

    screen.fill((0, 0, 0))

    # print(two_players)

    if player2.two_players:
        all_sprites.draw(screen)
    else:
        screen.blit(text, textRect)
    
    pygame.display.flip()

    clock.tick(30)
    # def server_updater(self, position):
    #     server_socket.sendall(position.encode())
    #     return server_socket.recv(1024).decode("utf-8")
