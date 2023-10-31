import pygame
from pygame.locals import *
import random


width = 800
height = 600
black = (0, 0, 0)
white = (255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()


def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGHT
    border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, white, border, 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 1
        self.rect.bottom = height - 10
        self.speed_x = 0
        self.shield = 100

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > height + 10 or self.rect.left < -40 or self.rect.right > width + 40:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-140, -100)
            self.speedy = random.randrange(1, 10)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # velocidad de la explocion

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
        else:
            center = self.rect.center
            self.image = explosion_anim[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center


def show_go_screen():

    draw_text(screen, "SHOOTER", 65, width // 2, height // 4)
    draw_text(screen, "Instrucion van aqui", 27, width // 2, height // 2)
    draw_text(screen, "Press Key", 20, width // 2, height * 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png",
               "assets/meteorGrey_big2.png",
               "assets/meteorGrey_big3.png",
               "assets/meteorGrey_big4.png",
               "assets/meteorGrey_med1.png",
               "assets/meteorGrey_med2.png",
               "assets/meteorGrey_small1.png",
               "assets/meteorGrey_small2.png",
               "assets/meteorGrey_tiny1.png",
               "assets/meteorGrey_tiny2.png"
               ]
for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())


# EXPLOCIN IMAGENES

explosion_anim = []
for i in range(9):
    file = "assets/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(black)
    img_scale = pygame.transform.scale(img, (70, 70))
    explosion_anim.append(img_scale)


# cargar imagen de fondo


background = pygame.image.load("assets/pngwing.png").convert()

# cargar sonidos

laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.2)

pygame.mixer.music.play(loops=-1)

# patalla------- game over
game_over = True


# procesando todo los eventos
running = True
while running:
    if game_over:

        show_go_screen()

        game_over = False
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)
        for i in range(8):
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)

        score = 0

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    # colicion - meteoro -laser

    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 10
        # explosio

        explosion_sound.play()
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    # checar colicion -jugador -meteoro
    # lo objetos que metoquen desaparecen
    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:
        player.shield -= 25
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        if player.shield <= 0:
            game_over = True

    screen.blit(background, [0, 0])
    all_sprites.draw(screen)

    # marcador

    draw_text(screen, str(score), 25, width // 2, 10)

    # Escudo
    draw_shield_bar(screen, 5, 5, player.shield)

    pygame.display.flip()


pygame.quit()
