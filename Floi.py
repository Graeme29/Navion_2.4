# -*- coding: utf-8 -*-
import pygame
import pygame.event as GAME_EVENTS
import pygame.locals as GAME_GLOBALS
import pygame.time as GAME_TIME
import sys

import tab
import waves

pygame.init()
clock = pygame.time.Clock()

Width = 700
Height = 700
fenetre = pygame.display.set_mode((Width, Height))  # , pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF

pygame.display.set_caption('Navion :)')

# Variables pour les vagues d'enemis
Nivo = 0
Wave = 0
Lastwavewhen = 0

# Variables de déplacements
Px = (Width / 2) - (111 / 2)  # Position latérale de base de l'avion
Py = Height - 137  # Position verticale de base de l'avion

# Variables pour les touches de clavier

DownPress = False  # | Les variables booléennes changent de valeurs
UpPress = False  # | en fonction de si oui ou non une touche est préssé
RightPress = False  # |
LeftPress = False  # |
APress = False  # |
SpacePress = False  # |

# Diverses options
Mouse = False  # Le Mode souris est désactivé par défaut
MenuL = False  # Le premier écran qui apparaît ne doit pas être le menu
GameL = False  # Le jeu ne dois pas commencer dés le lancement, il passe d'abord par le menu
StartL = True  # Voici l'écran de démarrage, qui s'affiche uniquement lors du lancement du programme
OptionL = False
OverL = False
firstlaunch = True
keyDown = False
MousePush = False
Twoplayers = False
Friendlyfire = False
FFx = False
FFy = False
MouseX = False
MouseY = False
MenuX = False  # Toute petite variable qui sert à ne pas appuyer directement sur le bouton "quitter" par erreur en retournant vers le menu

# Importation des images
fond = pygame.image.load("Images/ciel.png").convert()
fenetre.blit(fond, (0, 0))

titre = pygame.image.load("Images/Titre.png").convert_alpha()
ban = pygame.image.load("Images/space.png").convert_alpha()
Start = pygame.image.load("Images/Start.png").convert_alpha()
exitt = pygame.image.load("Images/exit.png").convert_alpha()
Option = pygame.image.load("Images/Options.png").convert_alpha()
multi = pygame.image.load("Images/multi.png").convert_alpha()
clavierimg = pygame.image.load("Images/clavier.png").convert_alpha()
sourisimg = pygame.image.load("Images/souris.png").convert_alpha()
over = pygame.image.load("Images/gameover.png").convert_alpha()
retour = pygame.image.load("Images/retour.png").convert_alpha()
ffon = pygame.image.load("Images/ff on.png").convert_alpha()
ffoff = pygame.image.load("Images/ff off.png").convert_alpha()

OneHp = pygame.image.load("Images/1HP.png").convert_alpha()
TwoHp = pygame.image.load("Images/2HP.png").convert_alpha()
ThreeHp = pygame.image.load("Images/3HP.png").convert_alpha()
FourHp = pygame.image.load("Images/4HP.png").convert_alpha()
FiveHp = pygame.image.load("Images/5HP.png").convert_alpha()
OnebisHp = pygame.image.load("Images/1HPbis.png").convert_alpha()
TwobisHp = pygame.image.load("Images/2HPbis.png").convert_alpha()
ThreebisHp = pygame.image.load("Images/3HPbis.png").convert_alpha()
FourbisHp = pygame.image.load("Images/4HPbis.png").convert_alpha()
FivebisHp = pygame.image.load("Images/5HPbis.png").convert_alpha()
TwotwoHp = pygame.image.load("Images/2HPtwo.png").convert_alpha()
ThreetwoHp = pygame.image.load("Images/3HPtwo.png").convert_alpha()
FourtwoHp = pygame.image.load("Images/4HPtwo.png").convert_alpha()
FivetwoHp = pygame.image.load("Images/5HPtwo.png").convert_alpha()

# Importation des sons
son = pygame.mixer.music.load("Son/v.mp3")
pygame.mixer.music.play(loops=-1)

# Importation des avions
Navion = tab.Navion(pygame, fenetre)
Mavion = tab.Mavion(pygame, fenetre)
Vilains = []
BallesPerdues = []


# -----------------Evenements---------------------------
def Events():
    global MousePos, keyDown, MousePush, GameL, MenuL, Navion

    # --------------Notre Avion-------------------#
    if Twoplayers:

        if RightPress:
            if tab.Navion.x < 670:
                tab.Navion.x += tab.Navion.Vx
        if LeftPress:
            if tab.Navion.x > -5:
                tab.Navion.x -= tab.Navion.Vx
        if UpPress:
            if tab.Navion.y > -5:
                tab.Navion.y -= tab.Navion.Vy
        if DownPress:
            if tab.Navion.y < 670:
                tab.Navion.y += tab.Navion.Vy
        if SpacePress is True and keyDown is False:
            Navion.pew()
            keyDown = True
        elif SpacePress is False and keyDown is True:
            keyDown = False

        tab.Mavion.x = mousePos[0] - 20
        tab.Mavion.y = mousePos[1] - 20
        if mouseStates[0] == 1 and MousePush is False:
            Mavion.pew()
            MousePush = True
        elif mouseStates[0] == 0 and MousePush is True:
            MousePush = False

    else:
        if Mouse == 0:
            if RightPress:
                if tab.Navion.x < 670:
                    tab.Navion.x += tab.Navion.Vx
            if LeftPress:
                if tab.Navion.x > -5:
                    tab.Navion.x -= tab.Navion.Vx
            if UpPress:
                if tab.Navion.y > -5:
                    tab.Navion.y -= tab.Navion.Vy
            if DownPress:
                if tab.Navion.y < 670:
                    tab.Navion.y += tab.Navion.Vy
            if SpacePress is True and keyDown is False:
                Navion.pew()
                keyDown = True
            elif SpacePress is False and keyDown == True:
                keyDown = False

        else:
            tab.Navion.x = mousePos[0] - 20
            tab.Navion.y = mousePos[1] - 20
            if mouseStates[0] == 1 and MousePush is False:
                Navion.pew()
                MousePush = True
            elif mouseStates[0] == 0 and MousePush is True:
                MousePush = False

    # ----------------------------------------------#

    # -----------Les méchants avions----------------#
    Suprimation = []
    for idx, V in enumerate(
            Vilains):  # IDX correspond à un petit numéro associé à chaque Avion ennemi, permettant alors de "traquer" l'état de chaque ennemi
        if V.y < Height:  # Si l'ennemi est toujours sur l'écran
            V.marche()  # Le faire descendre, pour le mouvement
            V.tryToFire()
            Battu = Navion.checkForHit(V)  # Vérifier s'il s'est fait touché par une balle
            if Battu:  # S'il l'avion ennemi n'a plus de vie :
                Suprimation.append(
                    idx)  # Il faut alors l'ajouter à la liste "Suprimation" qui contient les ennemis morts (pour pouvoir les supprimer)
            if Twoplayers:
                OneDown = V.checkForHit(Navion)
                TwoDown = V.checkForHit(Mavion)
                if Friendlyfire:
                    Navion.checkForHit(Mavion)
                    Mavion.checkForHit(Navion)
                if OneDown:
                    Navion.Alive = False
                if TwoDown:
                    Mavion.Alive = False
                if OneDown and TwoDown:
                    gameover()
            else:
                Touche = V.checkForHit(Navion)
                if Touche:
                    gameover()
        else:
            Suprimation.append(idx)  # S'il n'est pas sur l'écran il faut égallement le supprimer

    oC = 0

    for idx in Suprimation:
        for remainingBullets in Vilains[idx - oC].balles:
            BallesPerdues.append(remainingBullets)

        del Vilains[idx - oC]
        oC += 1

    oC = 0
    for idx, B in enumerate(BallesPerdues):
        B.move()
        hitShip = B.checkForHit(Navion)
        hitShiptwo = B.checkForHit(Mavion)

        if hitShip:
            del BallesPerdues[idx - oC]
            Navion.life -= 1
        if hitShiptwo:
            del BallesPerdues[idx - oC]
            Mavion.life -= 1

        elif B.y > Height:
            del BallesPerdues[idx - oC]
            oC += 1

        # ------------------------------------------------------


# ------------------Game Over---------------------------
def gameover():
    global MenuL, GameL, Nivo, Wave, firstlaunch, OverL, Vilains, BallesPerdues
    Wave = 0
    Nivo = 0
    firstlaunch = True
    Navion.life = 5
    Mavion.life = 5
    Vilains = []
    BallesPerdues = []
    Navion.Alive = True
    Mavion.Alive = True
    OverL = True
    GameL = False


# -----------------------Waves--------------------------

def Wavet():
    global Wave, Lastwavewhen, Nivo

    thisLevel = waves.level[Nivo]["structure"]  # Prend la strucure du niveau et la met dans thisLevel

    if Wave < len(
            thisLevel):  # Si le numéro de vague est inférieur au nombre de vague dans le niveau (Si le niveau n'est pas fini)
        thisWave = thisLevel[
            Wave]  # "thisWave" contient le positionnement des méchants sous forme de liste binaire pour UNE ligne d'UNE vague

        for idx, place in enumerate(thisWave):
            if place == 1:
                Vilains.append(tab.mechant(((Width / len(thisWave)) * idx), -60, pygame, fenetre, 1))

        Lastwavewhen = timeTick  # Sauvegarde le moment ou la vague a été lancée
        Wave += 1  # Passage à la vague suivante

    elif Nivo + 1 < len(waves.level):
        Nivo += 1
        Wave = 0
        # ship.shields = ship.maxShields
        # nextLevelTS = timeTick + 5000


# ------------------------------------------------------


# ---------------------Affichements---------------------
def Affichements():
    fenetre.blit(fond, (0, 0))  # Efface les anciennnes apparitions en superposant une nouvelle couche du fond
    Navion.Blitz()  # Fait apparaître l'avion (Joueur 1) sur le devant de la scéne
    Navion.drawBullets()  # Fait apparaître les balles des avions alliés
    if Twoplayers:
        Mavion.Blitz()  # Fait apparaître l'avion (Joueur 2, si le mode 2 joueurs est activé) sur le devant de la scéne
        if Navion.life == 5:
            fenetre.blit(FivebisHp, (0, Height - 98))
        elif Navion.life == 4:
            fenetre.blit(FourbisHp, (0, Height - 98))
        elif Navion.life == 3:
            fenetre.blit(ThreebisHp, (0, Height - 98))
        elif Navion.life == 2:
            fenetre.blit(TwobisHp, (0, Height - 98))
        elif Navion.life == 1:
            fenetre.blit(OnebisHp, (0, Height - 98))

        if Mavion.life == 5:
            fenetre.blit(FivetwoHp, (Width - 32, Height - 98))
        elif Mavion.life == 4:
            fenetre.blit(FourtwoHp, (Width - 32, Height - 98))
        elif Mavion.life == 3:
            fenetre.blit(ThreetwoHp, (Width - 32, Height - 98))
        elif Mavion.life == 2:
            fenetre.blit(TwotwoHp, (Width - 32, Height - 98))
        elif Mavion.life == 1:
            fenetre.blit(OnebisHp, (Width - 32, Height - 98))
    else:
        if Navion.life == 5:
            fenetre.blit(FiveHp, (round((Width / 2) - 49), round(Height - 32)))
        elif Navion.life == 4:
            fenetre.blit(FourHp, (round((Width / 2) - 49), round(Height - 32)))
        elif Navion.life == 3:
            fenetre.blit(ThreeHp, (round((Width / 2) - 49), round(Height - 32)))
        elif Navion.life == 2:
            fenetre.blit(TwoHp, (round((Width / 2) - 49), round(Height - 32)))
        elif Navion.life == 1:
            fenetre.blit(OneHp, (round((Width / 2) - 49), round(Height - 32)))

    for V in Vilains:
        V.Blitz()
        V.drawBullets()

    for B in BallesPerdues:
        B.draw()


# ------------------------------------------------------

# ----------------Boucle du jeu-------------------------

while 1:
    mousePos = pygame.mouse.get_pos()
    mouseStates = pygame.mouse.get_pressed()

    # ------------------Menu--------------------------------

    if StartL:
        fenetre.blit(titre, (round((Width / 2) - 205), round(Height / 7)))
        fenetre.blit(ban, (round((Width / 2) - 150), round(Height / 1.2)))
        if SpacePress:
            StartL = False
            MenuL = True

    elif MenuL:
        fenetre.blit(fond, (0, 0))
        pygame.mouse.set_visible(1)
        fenetre.blit(titre, (round((Width / 2) - 205), round(Height / 7)))
        fenetre.blit(exitt, (round((Width / 2) - 87), round(Height / 1.5)))
        if mouseStates[0] == 1:
            if (Width / 2) - 87 < mousePos[0] < (Width / 2) + 87 and (Height / 1.5) < mousePos[1] < (Height / 1.5) + 81:
                pygame.quit()
                sys.exit()
        fenetre.blit(Option, (round((Width / 2) - 87), round(Height / 2)))
        if mouseStates[0] == 1:
            if (Width / 2) - 87 < mousePos[0] < (Width / 2) + 87 and (Height / 2) < mousePos[1] < (Height / 2) + 74:
                OptionL = True
                MenuL = False
        fenetre.blit(Start, (round(Width / 3) - 87, round(Height / 3)))
        if mouseStates[0] == 1:
            if (Width / 3) - 87 < mousePos[0] < (Width / 3) + 87 and (Height / 3) < mousePos[1] < (Height / 3) + 74:
                Twoplayers = False
                GameL = True
                MenuL = False
        fenetre.blit(multi, (round(Width * 2 / 3) - 87, round(Height / 3)))
        if mouseStates[0] == 1:
            if (Width * 2 / 3) - 87 < mousePos[0] < (Width * 2 / 3) + 87 and (Height / 3) < mousePos[1] < (
                    Height / 3) + 74:
                Twoplayers = True
                GameL = True
                MenuL = False

        pygame.display.update()


    elif OptionL:
        fenetre.blit(fond, (0, 0))
        fenetre.blit(titre, (round((Width / 2) - 205), round(Height / 7)))

        if Mouse:
            fenetre.blit(sourisimg, (round(Width / 2) - 87, round(Height / 1.5)))
            if mouseStates[0] == 1:
                if (Width / 2) - 87 < mousePos[0] < (Width / 2) + 87 and (
                        Height / 1.5) < mousePos[1] < (Height / 1.5) + 74:
                    MouseX = True
            if mouseStates[0] == 0 and MouseX is True:
                Mouse = False
                MouseX = False
        else:
            fenetre.blit(clavierimg, (round((Width / 2) - 87), round(Height / 1.5)))
            if mouseStates[0] == 1:
                if (Width / 2) - 87 < mousePos[0] < (Width / 2) + 87 and (Height / 1.5) < mousePos[1] < (
                        Height / 1.5) + 74:
                    MouseY = True
            if mouseStates[0] == 0 and MouseY is True:
                Mouse = True
                MouseY = False

        fenetre.blit(retour, (round((Width / 2) - 87), round(Height / 1.2)))
        if mouseStates[0] == 1:
            if (Width / 2) - 87 < mousePos[0] < (Width / 2) + 87 and (Height / 1.2) < mousePos[1] < (Height / 1.2) + 81:
                MenuL = True
                OptionL = False

        if Friendlyfire:
            fenetre.blit(ffon, (round((Width / 2) - 87), round(Height / 2)))
            if mouseStates[0] == 1:
                if (Width / 2) - 87 < mousePos[0] < (Width / 2) + 87 and (Height / 2) < mousePos[1] < (Height / 2) + 74:
                    FFx = True
            if mouseStates[0] == 0 and FFx is True:
                Friendlyfire = False
                FFx = False
        else:
            fenetre.blit(ffoff, (round((Width / 2) - 87), round(Height / 2)))
            if mouseStates[0] == 1:
                if (Width / 2) - 87 < mousePos[0] < (Width / 2) + 87 and (Height / 2) < mousePos[1] < (
                        Height / 1.5) + 74:
                    FFy = True
            if mouseStates[0] == 0 and FFy is True:
                Friendlyfire = True
                FFy = False


    elif GameL is True:  # Si le jeu est lancé :
        if firstlaunch:  # Pour faire le calcul uniquement au début du jeu
            Thegamestartedwhen = GAME_TIME.get_ticks()  # Cette variable permet de "reset" le temps à 0, afin de pouvoir évaluer le temps de jeu (et non pas le temps passé sur le menu)
            firstlaunch = 0

        timeTick = GAME_TIME.get_ticks() - Thegamestartedwhen  # Calcule le temps de jeu en cours
        pygame.mouse.set_visible(0)  # Cache le curseur qui pourrais perturber le jeu
        Events()  # Contient tout les "événements de jeu" (Mouvements clavier/souris, mouvements des balles...)
        Affichements()  # Ce qui est transmit à l'écran (Draw...)
        delai = waves.level[Nivo]["delai"]
        if Twoplayers:
            if timeTick - Lastwavewhen > (
                    delai / 2):  # waves.level[Nivo]["delai"]: #Aprés chaque délai précisé dans chaque niveaux dans le fichier "wave", une nouvelle vague d'ennemis est créee
                Wavet()  # Création d'une nouvelle vague d'ennemis
        else:
            if timeTick - Lastwavewhen > (
                    delai):  # waves.level[Nivo]["delai"]: #Aprés chaque délai précisé dans chaque niveaux dans le fichier "wave", une nouvelle vague d'ennemis est créee
                Wavet()

    elif OverL is True:
        pygame.mouse.set_visible(1)
        fenetre.blit(over, (0, 0))
        if mouseStates[0] == 1:  # Recommencer
            if 185 < mousePos[0] < 560 and 450 < mousePos[1] < 490:
                GameL = True
                OverL = False

        if mouseStates[0] == 1:  # Quitter
            if 255 < mousePos[0] < 475 and 580 < mousePos[1] < 610:
                pygame.quit()
                sys.exit()

        if mouseStates[0] == 1:  # Menu
            if 295 < mousePos[0] < 440 and 520 < mousePos[1] < 550:
                MenuX = True
        if mouseStates[0] == 0 and MenuX is True:
            MenuL = True
            OverL = False
            MenuX = False
        pygame.display.update()

    # ------------------------------------------------------

    # --------------------Actualisation---------------------

    pygame.display.update()

    # ------------------------------------------------------

    # --------------Touches activées------------------------

    for event in GAME_EVENTS.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                DownPress = True
            if event.key == pygame.K_UP:
                UpPress = True
            if event.key == pygame.K_RIGHT:
                RightPress = True
            if event.key == pygame.K_LEFT:
                LeftPress = True
            if event.key == pygame.K_a:
                APress = True
            if event.key == pygame.K_SPACE:
                SpacePress = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_DOWN:
                DownPress = False
            if event.key == pygame.K_UP:
                UpPress = False
            if event.key == pygame.K_RIGHT:
                RightPress = False
            if event.key == pygame.K_LEFT:
                LeftPress = False
            if event.key == pygame.K_a:
                APress = False
            if event.key == pygame.K_SPACE:
                SpacePress = False

        if event.type == GAME_GLOBALS.QUIT:  # |Permet au logiciel de s'arrêter
            pygame.quit()  # |proprement lorsque l'on clique sur
            sys.exit()  # |le bouton quitter de la fenêtre

    # clock.tick(100)
# ------------------------------------------------------
# ------------------------------------------------------
