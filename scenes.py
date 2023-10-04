"""
Gestion des scènes du jeu
"""

from typing import Protocol

import pygame

from button import Button
from lives import Lives
from monkey import Monkey
from object import Object
from text import Text


class Scene(Protocol):
    """Scène du jeu"""

    def affiche_scene(self) -> None:
        ...

    def joue_tour(self) -> None:
        ...

    def passe_suivant(self) -> bool:
        ...


class Partie:
    """Partie de catapulte"""

    def __init__(self) -> None:
        largeur, hauteur = pygame.display.get_window_size()

        self.decors: Object = Object(
            "images/jungle.png", (largeur // 2, hauteur), largeur
        )
        self.catapulte: Object = Object(
            "images/catapulte.png", (120, 560), 400
        )
        self.singe: Monkey = Monkey((150, 280), 40, 10)
        self.bananes: pygame.sprite.Group = pygame.sprite.Group()
        self.pilliers: list[pygame.Rect] = []

        self.nb_objets: int = 3
        for i in range(self.nb_objets):
            rectangle = pygame.Rect(500 + i * 120, 0, 80, 200 + i * 100)
            rectangle.bottom = 550
            self.pilliers.append(rectangle)
            self.bananes.add(
                Object(
                    "images/banane.png",
                    (rectangle.centerx, rectangle.top - 5),
                    30,
                )
            )

        self.points: int = 0
        self.vies: Lives = Lives(5, (20, 20))
        self.son: pygame.mixer.Sound = pygame.mixer.Sound("sounds/Glug.wav")
        self.son.set_volume(0.25)

    def affiche_scene(self) -> None:
        """Affiche les éléments du jeu"""
        fenetre = pygame.display.get_surface()

        couleur_pilliers = pygame.Color(33, 73, 59)
        couleur_bordure = pygame.Color(0, 0, 0)

        fenetre.blit(self.decors.image, self.decors.rect)
        for rectangle in self.pilliers:
            pygame.draw.rect(fenetre, couleur_pilliers, rectangle)
            pygame.draw.rect(fenetre, couleur_bordure, rectangle, 1)
        self.bananes.draw(fenetre)
        fenetre.blit(self.catapulte.image, self.catapulte.rect)
        fenetre.blit(self.singe.image, self.singe.rect)
        fenetre.blit(self.vies.image, self.vies.rect)

    def joue_tour(self) -> None:
        """Joue un tour du jeu"""
        largeur, hauteur = pygame.display.get_window_size()
        # déplacements du songe
        self.singe.update()

        # collision avec une banane
        if pygame.sprite.spritecollide(self.singe, self.bananes, True):
            self.son.play()
            self.points += 1

        # fin de catapultage
        if self.singe.is_out_screen(largeur, hauteur):
            self.singe.goto_start()
            self.vies.lose(1)

        self.vies.update()

    def passe_suivant(self) -> bool:
        """Renvoie si la partie est terminée"""
        return self.perdu or self.gagne

    @property
    def perdu(self) -> bool:
        """Partie perdue"""
        return self.vies.is_dead

    @property
    def gagne(self) -> bool:
        """Partie gagnée"""
        return self.points == self.nb_objets


class Fin:
    """Scène de fin"""

    def __init__(self, victoire: bool) -> None:
        largeur, hauteur = pygame.display.get_window_size()

        self.decors: Object = Object(
            "images/jungle.png", (largeur // 2, hauteur), largeur
        )
        self.message_fin: Text = Text(
            "Gagné !" if victoire else "Perdu ...", (largeur // 2, 150)
        )
        self.bouton_rejouer: Button = Button(
            "Rejouer", (250, 80), (largeur // 2, 400)
        )

        self.son_fin: pygame.mixer.Sound = (
            pygame.mixer.Sound("sounds/win.wav")
            if victoire
            else pygame.mixer.Sound("sounds/lose.mp3")
        )
        self.son_fin.set_volume(0.25 if victoire else 0.5)
        self.son_fin.play()

        self.son_bouton: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/pop.wav"
        )
        self.son_bouton.set_volume(0.25)
        self.next: bool = False

    def affiche_scene(self) -> None:
        """Affiche la scène de fin"""
        fenetre = pygame.display.get_surface()
        fenetre.blit(self.decors.image, self.decors.rect)
        fenetre.blit(self.message_fin.image, self.message_fin.rect)
        fenetre.blit(self.bouton_rejouer.image, self.bouton_rejouer.rect)

    def joue_tour(self) -> None:
        """Rien"""
        self.bouton_rejouer.update()
        for _ in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if self.bouton_rejouer.touch_mouse():
                self.son_bouton.play()
                self.next = True

    def passe_suivant(self) -> bool:
        """Vérifie si le bouton rejouer est cliqué"""
        return self.next
