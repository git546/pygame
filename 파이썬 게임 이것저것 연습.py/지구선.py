import pygame
import random
import os
import sys
import time
import math
# ----- 게임창 위치설정 -----
win_posx = 100
win_posy = 50

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_posx, win_posy)
# ----- 전역 -----
screen_width = 1300
screen_height = 700
FPS = 60
score = 0
playtime = 1
pos_x=screen_width*0.5
pos_y=screen_height*0.5
speed=2
a_width=25
a_height=25
e_width=40
e_height=80
p_width=80
p_height=80
Wave=1
Gold=0
# ----- 색상 -----
BLACK = 0, 0, 0
WHITE = 255,255,255
RED = 255, 0, 0
GREEN1 = 25, 102, 25
GREEN2 = 51, 204, 51
GREEN3 = 233, 249, 185
BLUE = 17, 17, 212
BLUE2 = 0, 0, 255
YELLOW = 255, 255, 0
LIGHT_PINK1 = 255, 230, 255
LIGHT_PINK2 = 255, 204, 255
def initialize_game(width, height):
    pygame.init()
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pygame Shmup")
    return surface

def game_loop(surface):
    clock = pygame.time.Clock()
    sprite_group = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = PlayerShip()
    shot_sound = pygame.mixer.Sound('shot.wav')
    global player_health
    player_health= 100
    global score,Gold,Wave
    score = 0
    Gold=0
    sprite_group.add(player)
    for i in range(7):
        enemy = Mob()
        sprite_group.add(enemy)
        mobs.add(enemy)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_SPACE:
                    if Gold >= 100:
                        player_health += int(Gold/2) 
                        Gold =0
                        if player_health > 100:
                            player_health =100

            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot(sprite_group, bullets)
                pygame.mixer.Sound.play(shot_sound)
        Walk()   
        sprite_group.update()
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            
            mob = Mob()
            sprite_group.add(mobs)
            mobs.add(mob)
            sprite_group.add(mobs)
            mobs.add(mob)
            score += 10
            Gold += random.randint(3, 7)

        hits = pygame.sprite.spritecollide(player, mobs, True)
        if hits:
            print('a mob hits player!')
            player_health -= random.randint(3, 5)
            mob = Mob()
            sprite_group.add(mobs)
            mobs.add(mob)
            if player_health < 0:
                gameover(surface)
                close_game()
                restart()
        if score >=50*Wave:
            Wave+=1
            score=0
        surface.fill(BLACK)
        sprite_group.draw(surface)
        score_update(surface)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    print('당신이 살아 있던 년수',playtime)
    print('당신 문명의 수준',Wave)
    print('당신이 모은 자원',Gold)
    
def Walk():
    global pos_x, pos_y
    key_event = pygame.key.get_pressed()
    if key_event[ord('a')]:
            pos_x -= speed
    if key_event[ord('d')]:
            pos_x += speed
    if key_event[ord('w')]:
            pos_y -= speed
    if key_event[ord('s')]:
            pos_y += speed
def Shoot():
    global pos_x
def score_update(surface):
    font = pygame.font.SysFont('malgungothic',35)
    image = font.render(f' 다음 단계 까지 :{score} 우주선의 체력: {player_health} 자원:{Gold} 문명진척도:{Wave}', True, BLUE2)
    pos = image.get_rect()
    pos.move_ip(20,20)
    pygame.draw.rect(image, BLACK,(pos.x-20, pos.y-20, pos.width, pos.height), 2)
    surface.blit(image, pos)

def gameover(surface):
    font = pygame.font.SysFont('malgungothic',50)
    image = font.render('GAME OVER', True, BLACK)
    pos = image.get_rect()
    pos.move_ip(50, int(screen_height/2))
    surface.blit(image, pos)
    pygame.display.update()
    time.sleep(2)
def close_game():
    pygame.quit()
    print('Game closed')
def restart():
    screen = initialize_game(screen_width,screen_height)
    game_loop(screen)
    close_game()

class PlayerShip(pygame.sprite.Sprite):
   def __init__(self):
        super().__init__()
        a=pygame.image.load("img/char1.png")
        a=pygame.transform.scale(a, (p_width, p_height))
        self.original_image= a
        self.angle= 0
         
   def update(self):
        mouse_x= pygame.mouse.get_pos()[0]
        mouse_y= pygame.mouse.get_pos()[1]
         
        self.angle= math.pi- math.atan2(mouse_x- pos_x, mouse_y- pos_y)
        self.image= pygame.transform.rotate(self.original_image,-(int(math.degrees(self.angle))))
         
        self.rect= self.image.get_rect()
        self.rect.center= (pos_x,pos_y)
   def shoot(self, all_sprites,bullets):
        bullet = Bullet()
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        e_width=random.randint(30, 150)
        e_height=random.randint(30, 200)
        a=pygame.transform.scale(pygame.image.load("img/ston.png"), (e_width, e_height))
        self.image = a
        self.helath = 30
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(0, screen_height)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.direction_change = False
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > screen_height + 10 or self.rect.left < -25 or self.rect.right >screen_width + 20:
            self.rect.x = random.randrange(screen_height - self.rect.width)
            self.rect.y = random.randrange(0, screen_height)
            self.speedy = random.randrange(3, 8)

class Bullet(pygame.sprite.Sprite):# Bullet
    def __init__(self):
        super().__init__()
        a=pygame.transform.scale(pygame.image.load("img/bullet.png"), (a_width, a_height))
        self.bullet_image= a
         
        mouse_x= pygame.mouse.get_pos()[0]
        mouse_y= pygame.mouse.get_pos()[1]    
        self.angle= math.pi- math.atan2(mouse_x- pos_x, mouse_y- pos_y)
        self.image= pygame.transform.rotate(self.bullet_image,-(int(math.degrees(self.angle))))
         
        self.speed= 10
        self.x= 0
        self.y= 0
         
    def update(self):
     
        self.x+= self.speed* math.sin(self.angle)
        self.y-= self.speed* math.cos(self.angle)
        self.rect= self.image.get_rect()
        self.rect.center= (pos_x+ self.x,pos_y+ self.y)

if __name__ == '__main__':
    screen = initialize_game(screen_width,screen_height)
    game_loop(screen)
    sys.exit()


