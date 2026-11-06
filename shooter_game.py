from pygame import *
from random import randint
font.init()
init()

# Configuración de pantalla
ancho = 700
alto = 900
fps = 60

window = display.set_mode((ancho, alto))
display.set_caption("Galaxia")
clock = time.Clock()

# Cargar fondo
background = transform.scale(image.load('galaxy.jpg'), (ancho, alto))

# Clase padre para objetos del juego
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def isCollision(self, obj):
        return self.rect.colliderect(obj.rect)

# Clase del jugador principal
class Player(GameSprite):
    def Moves(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < ancho - self.rect.width:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 10, self.rect.top, 20, 35, 12)
        bullets.add(bullet)

# Clase enemigo
class Enemy(GameSprite):
    def moveDown(self):
        self.rect.y += self.speed
        if self.rect.y > alto:
            self.rect.x = randint(0, ancho - self.rect.width)
            self.rect.y = -50

# Clase bala
class Bullet(GameSprite):
    def moveUp(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

# Instancias
jugador = Player('rocket.png', 300, 750, 80, 80, 10)

enemigos = sprite.Group()
for i in range(randint(4, 8)):
    tmpSpeed = randint(1, 4)
    tempX = randint(0, ancho - 80)
    enemigo = Enemy('ufo.png', tempX, randint(-150, -50), 80, 80, tmpSpeed)
    enemigos.add(enemigo)

bullets = sprite.Group()

# Bucle principal
Correr = True
finish = False

fnt = font.Font(None, 90)
gameover = fnt.render('Perdistes', True, (255, 215, 0))

while Correr:
    for evento in event.get():
        if evento.type == QUIT:
            Correr = False
        elif evento.type == KEYDOWN:
            if evento.key == K_SPACE and not finish:
                jugador.shoot()

    if not finish:
        window.blit(background, (0, 0))

        # Movimientos
        jugador.Moves()
        
        for enemy in enemigos:
            enemy.moveDown()

        for bullet in bullets:
            bullet.moveUp()

        # Colisiones balas - enemigos
        collided = sprite.groupcollide(enemigos, bullets, True, True)
        for c in collided:
            # Reaparecer un nuevo enemigo si destruyes uno
            tmpSpeed = randint(1, 4)
            tempX = randint(0, ancho - 80)
            enemigo = Enemy('ufo.png', tempX, randint(-150, -50), 80, 80, tmpSpeed)
            enemigos.add(enemigo)

        # Colisión enemigo - jugador
        for enemy in enemigos:
            if enemy.isCollision(jugador):
                finish = True

        # Dibujar elementos
        jugador.reset()
        enemigos.draw(window)
        bullets.draw(window)

        display.update()

    clock.tick(fps)

quit()

