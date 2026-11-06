from pygame import *
from random import randint
font.init()
init()

ancho = 700
alto = 900
fps = 60

window = display.set_mode((ancho, alto))
display.set_caption("Galaxia")

clock = time.Clock()

background = transform.scale(image.load('galaxy.jpg'), (ancho, alto))

# clase padre para otros objetos
class GameSprite(sprite.Sprite):
    # constructor de clase
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
            window.blit(self.image, (self.rect.x, self.rect.y))

    # método que dibuja al personaje en la ventana
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def isCollision(self, object):
        return self.rect.colliderect(object.rect)

enemigos = []
Bullets = []
# clase del jugador principal

class Bullet(GameSprite):
    def moveUp(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            Bullets.remove(self)    

class Player(GameSprite):

    def Moves(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        
        if keys[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed

    def shoot(self):
            bullet = Bullet('bullet.png', self.rect.centerx - 10, self.rect.top, 20, 35, 12)
            Bullets.append(bullet)

class Enemy(GameSprite):
    
    def moveDown(self):
        self.rect.y += self.speed
        if self.rect.y > alto + 20:
            self.rect.y = 0

jugador = Player('rocket.png', 300, 750, 100, 100, 10)

for i in range(randint(4, 10)):
    tmpSpeed = randint(1, 5)
    tempX = randint(1, ancho)
    enemigo = Enemy('ufo.png', tempX, 0, 100, 100, tmpSpeed)
    enemigos.append(enemigo)

Correr = True
finish = False
startbutton = False

fnt = font.Font(None, 90)
gameover = fnt.render('GameOver', True, (255, 215, 0))

while Correr:

    for evento in event.get():
        if evento.type == QUIT:
            Correr = False
        if evento.type == KEYDOWN:
            if evento.key == K_SPACE and not finish:
                jugador.shoot()
            if evento.key == K_r:
                startbutton = True
                

    window.blit(background, (0, 0))

    if not finish:
        jugador.reset()
        jugador.Moves()
    
        for enemy in enemigos:
            enemy.reset()
            enemy.moveDown()

        for bullet in Bullets:
            bullet.reset()
            bullet.moveUp()

            if bullet.isCollision(enemy):
                if enemy in enemigos:
                    enemigos.remove(enemy)

    if jugador.isCollision(enemy):
        window.blit(gameover, (200, 350))
        display.update()
        time.delay(500)
        finish = True
        enemigos.clear()
        Bullets.clear()
            
    if not finish:
        jugador.draw()
        clock.tick(fps)
        display.update()



