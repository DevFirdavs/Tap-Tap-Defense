import pygame
from pygame import mixer
import os, random
from abc import ABC, abstractmethod
from settings import *


class StartMenu:
    def __init__(self, font):
        self.animate = 0
        self.background_image = pygame.image.load(os.path.join("game_assets", "start-menu.png"))
        self.rescaled_background_image = pygame.transform.scale(self.background_image, (width, height))
        self.text = font.render('Press any key to start', False, white)
        self.weapon_select = font.render("Glock", True, white)
        self.weapon_select_rect = self.weapon_select.get_rect(center=(350, 200))
        self.skill_select = font.render("Skill1", True, white)
        self.skill_select_rect = self.skill_select.get_rect(center=(350, 250))

    def draw(self, screen):
        screen.blit(self.rescaled_background_image, (0, 0))
        if self.animate < 0:
            pygame.draw.rect(screen, black, [237, 340, 220, 40])
            screen.blit(self.text, (243, 350))
        if self.animate == -15:
            self.animate = 15
        pygame.draw.rect(screen, brown, [305, 180, 90, 40])
        pygame.draw.rect(screen, brown, [305, 230, 90, 40])
        screen.blit(self.weapon_select, self.weapon_select_rect)
        screen.blit(self.skill_select, self.skill_select_rect)
        self.animate -= 1

class EndMenu:
    def __init__(self, font):
        my_font = pygame.font.SysFont(font_name, 26)
        tempimage = pygame.image.load(os.path.join("game_assets", "castle_3.png"))
        tempimage = pygame.transform.scale(tempimage, (180, 180))
        tempimage_rect = tempimage.get_rect(center=(350, 90))
        self.img = tempimage
        self.rect = tempimage_rect
        self.text = font.render('GAME OVER', False, darker_cyan)
        self.text2 = my_font.render('Press CAPSLOCK to replay the game', False, white)
        self.text3 = my_font.render('Press ESC to exit', False, white)
        self.text_rect = self.text.get_rect(center=(350, 210))
        self.text2_rect = self.text2.get_rect(center=(350, 240))
        self.text3_rect = self.text3.get_rect(center=(350, 270))

    def draw(self, screen):
        screen.fill(cyan)
        screen.blit(self.img, self.rect)
        screen.blit(self.text, self.text_rect)
        screen.blit(self.text2, self.text2_rect)
        screen.blit(self.text3, self.text3_rect)

class Player():
    def __init__(self):
        self.score = 0
        self.damage = 0
        self.mana = 0
        self.crosshair = pygame.image.load(os.path.join("game_assets", "crosshair.png")).convert_alpha()
        self.img = []
        for i in range(4):
            tempImage = pygame.image.load(os.path.join("game_assets", "castle_" + str(i) + ".png"))
            tempImage = pygame.transform.scale(tempImage, (250, 250))
            self.img.append(tempImage)

    def get_kill(self):
        self.score += 1
        if self.mana != 10:
            self.mana += 1

    def take_damage(self):
        self.damage += 1

    def use_skill(self, cost):
        self.mana -= cost

    def update(self, screen, font):
        temp = ""
        for i in range(self.mana):
            temp += "[]"
        self.x, self.y = pygame.mouse.get_pos()
        self.x -= 30
        self.y -= 30
        score = font.render("Score : " + str(self.score), True, white)
        mana = font.render("Mana : " + temp, True, white)
        screen.blit(self.img[self.damage], (0, 25))
        screen.blit(self.crosshair, (self.x, self.y))
        screen.blit(score, (textX, textY))
        screen.blit(mana, (textX, textY + (2 * space)))

class BomboSapiens(ABC):
    def __init__(self, name, hp, spd, image):
        self.name = name
        self.animation = 0
        self.walk = image
        self.hp = hp
        self.__spd = spd
        self.move = self.__spd
        self.explodeImage = []
        for i in range(9):
            tempImage = pygame.image.load(os.path.join("game_assets", "explosion0" + str(i) + ".png"))
            tempImage = pygame.transform.scale(tempImage, (80, 80))
            self.explodeImage.append(tempImage)
        self.explode_sound = mixer.Sound(os.path.join("game_assets", "explosion.mp3"))
        self.explode_duration = 8
        self.isexplode = False
        self.isstun = False
        self.time = 0
        self.x = 700
        self.y = random.choice(mob_position)

    @abstractmethod
    def maju(self):
        if self.animation < len(self.walk) - 1:
            self.animation += 1
        else:
            self.animation = 0
        self.image = self.walk[self.animation]
        self.x -= self.move

    @abstractmethod
    def take_damage(self, player, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.explode()
            player.get_kill()

    @abstractmethod
    def explode(self):
        self.move = 0
        self.time = 0
        self.explode_sound.play()
        self.isexplode = True

    @abstractmethod
    def stun(self, time):
        self.time = 0
        self.move = 0
        self.stun_duration = time
        self.isstun = True

    @abstractmethod
    def remove(self, list, i):
        list.remove(i)
        return list

    @abstractmethod
    def update(self, screen, player, list, i):
        if not self.isexplode:
            self.maju()
        if self.x < base and not self.isexplode:
            self.explode()
            player.take_damage()
        if self.isexplode:
            self.time += 1
            self.image = self.explodeImage[self.time]
            if self.time == self.explode_duration:
                self.remove(list, i)
                self.time = 0
        if self.isstun and not self.isexplode:
            self.time += 1
            if self.time == self.stun_duration:
                self.isstun = False
                self.move = self.__spd
                self.time = 0
        screen.blit(self.image, (self.x, self.y))

class NormalBombo(BomboSapiens):
    def __init__(self):
        name = "NB"
        image = []
        for i in range(11):
            tempimage = pygame.image.load(os.path.join("game_assets", "bombo" + str(i + 1) + ".png"))
            tempimage = pygame.transform.scale(tempimage, normal_bombo_size)
            image.append(tempimage)
        hp = 10
        spd = 2
        self.spot = [()]
        super().__init__(name, hp, spd, image)

    def maju(self):
        super().maju()

    def take_damage(self, player, dmg):
        super().take_damage(player, dmg)

    def explode(self):
        super().explode()

    def stun(self, time):
        super().stun(time)

    def remove(self, list, i):
        super().remove(list, i)

    def update(self, screen, player, list, i):
        super().update(screen, player, list, i)
        self.spot[0] = (self.x - 2, self.y - 2)

class GiantBombo(BomboSapiens):
    angryimage = []
    for i in range(4, 8):
        tempimage = pygame.image.load(os.path.join("game_assets", "giant" + str(i) + ".png"))
        tempimage = pygame.transform.scale(tempimage, giant_bombo_size)
        angryimage.append(tempimage)

    def __init__(self):
        name = "GB"
        image = []
        for i in range(4):
            tempimage = pygame.image.load(os.path.join("game_assets", "giant" + str(i) + ".png"))
            tempimage = pygame.transform.scale(tempimage, giant_bombo_size)
            image.append(tempimage)
        self.angry_sound = mixer.Sound(os.path.join("game_assets", "Giant Bombo Angry.mp3"))
        hp = 30
        spd = 1
        self.spot = [(), (), ()]
        super().__init__(name, hp, spd, image)

    def maju(self):
        super().maju()

    def take_damage(self, player, dmg):
        self.angry_sound.play()
        self.walk = GiantBombo.angryimage
        self.move += 1
        super().take_damage(player, dmg)

    def explode(self):
        self.angry_sound.stop()
        super().explode()

    def stun(self, time):
        super().stun(time)

    def remove(self, list, i):
        super().remove(list, i)

    def update(self, screen, player, list, i):
        super().update(screen, player, list, i)
        self.spot[0] = (self.x - 10, self.y + 5)
        self.spot[1] = (self.x - 3, self.y + 5)
        self.spot[2] = (self.x + 5, self.y + 5)

class Senjata(ABC):
    def __init__(self, name, mag, dmg, time, start, reload, shoot):
        self.name = name
        self.mag = mag
        self.ammo = self.mag
        self.dmg = dmg
        self.reload_time = time
        self.time = 0
        self.isshoot = True
        self.isreload = False
        self.start_sound = start
        self.reload_sound = reload
        self.shoot_sound = shoot

    @abstractmethod
    def start(self):
        self.start_sound.play()

    @abstractmethod
    def shoot(self):
        if self.isshoot:
            self.ammo -= 1
            self.shoot_sound.play()

    @abstractmethod
    def reload(self):
        if not self.isreload:
            self.reload_sound.play()
            self.isreload = True
            self.isshoot = False

    @abstractmethod
    def update(self, screen, font):
        temp = ""
        for i in range(self.ammo):
            temp += "[||) "
        ammo = font.render("Ammo : " + temp, True, white)
        screen.blit(ammo, (textX, textY + (4 * space)))
        if self.ammo == 0 and not self.isreload:
            self.reload()
        if self.isreload:
            self.time += 1
        if self.time == self.reload_time:
            self.ammo = self.mag
            self.isshoot = True
            self.isreload = False
            self.time = 0

class Glock(Senjata):
    def __init__(self):
        name = 'G'
        mag = 15
        dmg = 10
        time = 45
        start = mixer.Sound(os.path.join("game_assets", "glock_start.mp3"))
        reload = mixer.Sound(os.path.join("game_assets", "glock_reload.mp3"))
        shoot = mixer.Sound(os.path.join("game_assets", "glock_shoot.mp3"))
        super().__init__(name, mag, dmg, time, start, reload, shoot)

    def start(self):
        super().start()

    def shoot(self):
        super().shoot()

    def reload(self):
        super().reload()

    def update(self, screen, font):
        super().update(screen, font)

class Revolver(Senjata):
    def __init__(self):
        name = 'R'
        mag = 6
        dmg = 30
        time = 150
        start = mixer.Sound(os.path.join("game_assets", "revolver_start.mp3"))
        reload = []
        for i in range(7):
            temp = mixer.Sound(os.path.join("game_assets", "revolver_reload" + str(i) + ".mp3"))
            reload.append(temp)
        shoot = mixer.Sound(os.path.join("game_assets", "revolver_shoot.mp3"))
        super().__init__(name, mag, dmg, time, start, reload, shoot)
        self.boost = 0

    def start(self):
        super().start()

    def shoot(self, list, i):
        super().shoot()

    def reload(self):
        if not self.isreload:
            self.time += (10 * self.boost)
            self.reload_sound[self.boost].play()
            self.boost = 0
            self.isreload = True
            self.isshoot = False

    def update(self, screen, font):
        super().update(screen, font)

class Skill1:
    def __init__(self):
        self.name = '0'
        self.cost = 3
        self.knockback = 100
        self.effect = 15
        self.x = 200
        self.isactive = False
        self.image = pygame.image.load(os.path.join("game_assets", "angin.png"))
        self.sound = mixer.Sound(os.path.join("game_assets", "skill1.mp3"))
    
    def active(self, player, list, mana):
        if mana >= self.cost:
            player.use_skill(self.cost)
            self.isactive = True
            self.sound.play()
            for i in list:
                if i.name == "NB":
                    i.x += self.knockback
                elif i.name == 'GB':
                    i.stun(self.effect)
    
    def update(self, screen):
        if self.isactive:
            screen.blit(self.image, (self.x, 0))
            self.x += 100
            if self.x >= 700:
                self.x = 200
                self.isactive = False
        
class Skill2:
    def __init__(self):
        self.name = '1'
        self.isactive = False
        self.animate = 0
        self.location = []
        self.cost = 5
        self.dmg = 5
        self.effect = 30
        self.sound = mixer.Sound(os.path.join("game_assets", "electric_zap_001-6374.mp3"))
        self.image = []
        for i in range(27):
            tempimage = pygame.image.load(os.path.join("game_assets", "skill-2 (" + str(i + 1) + ").png"))
            tempimage = pygame.transform.scale(tempimage, (80, 80))
            self.image.append(tempimage)

    def active(self, player, list, mana):
        if mana >= self.cost:
            self.isactive = True
            player.use_skill(self.cost)
            self.sound.play()
            for i in list:
                self.location.append([i.x - 3, i.y - 2])
                i.take_damage(player, self.dmg)
                i.stun(self.effect)

    def update(self, screen):
        if self.isactive:
            for i in self.location:
                screen.blit(self.image[self.animate], (i[0], i[1]))
            self.animate += 1
        if self.animate == len(self.image):
            self.animate = 0
            self.location = []
            self.isactive = False

class Skill3:
    def __init__(self):
        self.name = '2'
        self.isactive = False
        self.animate = 0
        self.location = []
        self.cost = 10
        self.sound = mixer.Sound(os.path.join("game_assets", "skill_chant.ogg"))
        self.image = []
        for i in range (7):
            tempimage = pygame.image.load(os.path.join("game_assets", "skill3" + str(i) + ".png"))
            tempimage = pygame.transform.scale(tempimage, (80, 80))
            self.image.append(tempimage)

    def active(self, player, list, mana):
        if mana >= self.cost:
            self.isactive = True
            player.use_skill(self.cost)
            self.sound.play()
            for i in list:
                self.location.append([i.x, i.y])
                player.get_kill()
            list.clear()

    def update(self, screen):
        if self.isactive:
            for i in self.location:
                screen.blit(self.image[self.animate], (i[0], i[1]))
            self.animate += 1
        if self.animate == len(self.image):
            self.animate = 0
            self.location = []
            self.isactive = False
