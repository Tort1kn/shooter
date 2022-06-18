from pygame import *
from random import randint
from time import time as timer

# скачуємо окремі функції для роботи зі шрифтами

font.init()
font1 = font.SysFont(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.SysFont(None, 36)

#фонова музика
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# нам потрібні такі картинки картинки:
img_back = "galaxy.jpg" # фон гри
img_ast = "asteroid.png"
img_bullet = "bullet.png" # пуля
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # ворог
 
score = 0 # збито кораблів
goal = 10 # скільки трбе збити для перемоги
lost = 0 # пропущено кораблів
max_lost = 3 # програли якщо пропустили скільки
life = 3

# класс-батько для інших спрайтів
class GameSprite(sprite.Sprite):
  # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)

        # кожний спрайт повиннен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # кожний спрайт спрайт зберігає властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # метод, який малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# клас головного героя
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
  # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

# клас спрайта-ворога   
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дойде до краю экрану
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
 
# клас спрайта-кулі   
class Bullet(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        # зникає, якщл дойде до краю екрану
        if self.rect.y < 0:
            self.kill()
 
# створюємо вікно
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# створюємо спрайти
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
# створюємо групи спрайтів- ворогів
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

# створюємо групу спрайтів астероїдів ()
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)
 
bullets = sprite.Group()
 
# змінна "гра закінчилась": як тільки там True, в основнму циклі перестають працювати спрайти
finish = False
# Основний цикл гри:
run = True # прапор який спрацьовує на кнопку закриття вікна

rel_time = False #перезарядка

num_fire = 0 #кількість пострілів

while run:
    # подія натисканняна кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
        # подія натискання на пропуск - спрайт стріляє
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                # перевіряємо скільки пострілів зроблено і чи не відбувається перезарядка
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:  # якщо гравець зробив 5 пострілів
                    last_time = timer()  # засікаєсо час, коли це сталось
                    rel_time = True

 
  # сама гра: події спрайтів, перевірка правил гри, перемалювання
    if not finish:
        # оновлюємо фон
        window.blit(background,(0,0))

        # пишемо текст на екрані
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # запускаємо рух спрайтів
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        # оновлюємо їх в новому розташуванні при кожній ітерації циклу
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        # перезарядка
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
 
        # перевірка зіткнення пулі і монстра (і монстр, і пуля при зіткненні зникають)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # цей цикл повторюється стільки разів, скільки монстрів піб=дбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # якщо спрайт торкнувся ворога зменшуємо життя
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1

        #програш
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))


        # проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        # задаем разный цвет в зависимости от кол-ва жизней
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()
    # цикл спрацьовує кожну 0.05 с
    time.delay(50)
