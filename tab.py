import gun
import random


class Navion():
    x = 350
    y = 550
    Vx = 1  # Vitesse de déplacement latérale de l'avion
    Vy = 1  # Vitesse de déplacement verticale de l'avion
    width = 38
    height = 34
    Tir = False
    image = None
    fenetre = None
    balpng = "Images/bullet.png"
    balson = "Son/bullet.wav"
    balles = []
    tps = 5
    life = 5
    Left = False
    Alive = True

    def Image(self):
        self.image = self.pygame.image.load("Images/AVION.png")

    def Blitz(self):
        if self.Alive:
            self.fenetre.blit(self.image, (self.x, self.y))

    def __init__(self, pygame,
                 fenetre):  # Se lance dés l'utilisation de la classe Navion ,et permet de lui ajouter des paramétrzs
        self.pygame = pygame
        self.fenetre = fenetre
        self.Image()  # Initialise l'image

    def pew(self):
        if self.Alive:
            if self.Left:
                self.balles.append(gun.Pew(self.x + 7, self.y, self.pygame, self.fenetre, self.tps, self.balpng))
                self.Left = False
            else:
                self.balles.append(gun.Pew(self.x + 31, self.y, self.pygame, self.fenetre, self.tps, self.balpng))
                self.Left = True
            a = self.pygame.mixer.Sound(self.balson)
            a.set_volume(5)
            a.play()

    def drawBullets(self):
        if self.Alive:
            Balleperdue = []
            for idc, b in enumerate(self.balles):
                if b.y < 0:
                    Balleperdue.append(idc)
            bC = 0
            for usedBullet in Balleperdue:
                del self.balles[usedBullet - bC]
                bC += 1

            for b in self.balles:
                b.move()
                b.draw()

    def checkForHit(self, Letrucquisefaittaper):
        if self.Alive:
            Balleperdue = []

            for idx, b in enumerate(self.balles):
                if Letrucquisefaittaper.x < b.x < Letrucquisefaittaper.x + Letrucquisefaittaper.width:
                    if Letrucquisefaittaper.y < b.y < Letrucquisefaittaper.y + Letrucquisefaittaper.height:
                        Letrucquisefaittaper.life -= 1
                        Balleperdue.append(idx)

            bC = 0
            for usedBullet in Balleperdue:
                del self.balles[usedBullet - bC]
                bC += 1
            if Letrucquisefaittaper.life <= 0:
                return True


class Mavion(Navion):
    x = 50
    y = 50
    balpng = "Images/Mullet.png"
    firing = False
    Malive = True

    def pew(self):
        if self.Alive:
            if self.Left:
                self.balles.append(gun.Pew(self.x + 9, self.y, self.pygame, self.fenetre, self.tps, self.balpng))
                self.Left = False
            else:
                self.balles.append(gun.Pew(self.x + 33, self.y, self.pygame, self.fenetre, self.tps, self.balpng))
                self.Left = True
            a = self.pygame.mixer.Sound(self.balson)
            a.set_volume(5)
            a.play()

    def Image(self):
        self.image = self.pygame.image.load("Images/MAVION.png")


class mechant(Navion):
    x = 0
    y = 0
    firing = False
    image = None
    soundEffect = 'sounds/enemy_laser.wav'
    balpng = "Images/badbullet.png"
    tps = -5
    speed = 0.2
    life = 1
    width = 90
    height = 74

    def __init__(self, x, y, pygame, fenetre, life):
        super().__init__(pygame, fenetre)
        self.x = x
        self.y = y
        self.pygame = pygame
        self.fenetre = fenetre
        self.balles = []
        self.Image()
        self.life = life

        dimensions = self.image.get_rect().size
        self.width = dimensions[0]
        self.height = dimensions[1]

        self.x -= self.width / 2

    def pew(self):
        if self.Left:
            self.balles.append(gun.Pew(self.x + 12, self.y + 50, self.pygame, self.fenetre, self.tps, self.balpng))
            self.Left = False
        else:
            self.balles.append(gun.Pew(self.x + 78, self.y + 50, self.pygame, self.fenetre, self.tps, self.balpng))
            self.Left = True
            a = self.pygame.mixer.Sound(self.balson)
            a.set_volume(5)
            a.play()

    def marche(self):
        self.y += self.speed

    def Image(self):
        self.image = self.pygame.image.load("Images/mechant.png")

    def tryToFire(self):
        shouldFire = random.random()

        if shouldFire <= 0.01:
            self.pew()

    def checkforcollision(self, Letrucquisefaittaper):
        if Letrucquisefaittaper.x < self.x < Letrucquisefaittaper.x + Letrucquisefaittaper.width:
            if Letrucquisefaittaper.y < self.y < Letrucquisefaittaper.y + Letrucquisefaittaper.height:
                Letrucquisefaittaper.life -= 1
        if Letrucquisefaittaper.life <= 0:
            return True


