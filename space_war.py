# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 960
HEIGHT = 660
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)


# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 96)


# Images
ship_img = pygame.image.load('assets/images/player.png').convert_alpha()
laser_img = pygame.image.load('assets/images/laserRed.png').convert_alpha()
enemy_img = pygame.image.load('assets/images/enemyShip.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/laserGreen.png').convert_alpha()
powerup_img = pygame.image.load('assets/images/laserGreenShot.png').convert_alpha()

# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')


# Stages
START = 0
PLAYING = 1
WIN = 2
LOSE = 3


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 3
        self.shield = 3
        self.shoots_double = False

    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        print("Pew!")

        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self):
        ''' check screen edges '''
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        ''' check powerups '''
        hit_list = pygame.sprite.spritecollide(self, powerups, True, 
                                               pygame.sprite.collide_mask)

        for hit in hit_list:
            hit.apply(self)

        ''' check bombs '''
        hit_list = pygame.sprite.spritecollide(self, bombs, True, 
                                               pygame.sprite.collide_mask)

        for hit in hit_list:
            print("Oof!")
            self.shield -= 1

        if self.shield == 0:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()     
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        print("Bwwamp!")

        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, 
                                               pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            print("Boom!")
            player.score += 100
            print(player.score)
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()     
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class ShieldPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()     
        self.rect.x = x
        self.rect.y = y
        self.speed = 6

    def apply(self, ship):
        print('Woot beep')
        ship.shield = 3
        self.kill()
        
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()
    
class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 5
        self.moving_right = True
        self.drop_speed = 20
        self.bomb_rate = 60 # lower is faster

    def move(self):
        hits_edge = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True
            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            #self.move_down()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop_speed

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()
            
    def update(self):
        self.move()
        self.choose_bomber()
    
# Game helper functions
def show_title_screen():
    title_text = FONT_XL.render("Space War!", 1, WHITE)
    screen.blit(title_text, [128, 204])

def show_win_screen():
    title_text = FONT_XL.render("You win!", 1, WHITE)
    screen.blit(title_text, [128, 204])

def show_lose_screen():
    title_text = FONT_XL.render("You lose!", 1, WHITE)
    screen.blit(title_text, [128, 204])

def show_stats():
    score_text = FONT_LG.render(str(player.score), 1, WHITE)
    score_rect = score_text.get_rect()
    score_rect.right = WIDTH - 20
    score_rect.top = 20
    screen.blit(score_text, score_rect)

def check_end():
    global stage
    
    if len(mobs) == 0:
        stage = WIN
    elif len(player) == 0:
        stage = LOSE
    
    
def setup():
    global stage, done
    global player, ship, lasers, mobs, fleet, bombs, powerups
    
    ''' Make game objects '''
    ship = Ship(ship_img)
    ship.rect.centerx = WIDTH / 2
    ship.rect.bottom = HEIGHT - 30

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    mob1 = Mob(100, 100, enemy_img)
    mob2 = Mob(300, 100, enemy_img)
    mob3 = Mob(500, 100, enemy_img)
    
    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3)

    fleet = Fleet(mobs)

    powerup1 = ShieldPowerUp(200, -2000, powerup_img)
    powerups = pygame.sprite.Group()
    powerups.add(powerup1)
    
    ''' set stage '''
    stage = START
    done = False

    
# Game loop
setup()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
                
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
                    
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()

    pressed = pygame.key.get_pressed()

    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update()
        lasers.update()
        bombs.update()
        fleet.update()
        mobs.update()
        powerups.update()

        check_end()
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    lasers.draw(screen)
    bombs.draw(screen)
    player.draw(screen)
    mobs.draw(screen)
    powerups.draw(screen)
    show_stats()
    
    if stage == START:
        show_title_screen()
    elif stage == WIN:
        show_win_screen()
    elif stage == LOSE:
        show_lose_screen()

        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
