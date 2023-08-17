"""
Gestion des scènes du jeu
"""

from typing import Protocol

import pygame

from elements import Fond, Objet, Personnage
from texte import Bouton, Message


class Scene(Protocol):
    """Scène du jeu"""

    def affiche_scene(self, fenetre: pygame.Surface) -> None:
        ...

    def joue_tour(self) -> None:
        ...

    def passe_suivant(self) -> bool:
        ...


class Partie:
    """Partie de catapulte"""

    # TODO afficher le score et les vies

    def __init__(self, largeur: int, hauteur: int) -> None:
        self.decors: Fond = Fond("jungle.png", largeur, hauteur)
        self.catapulte: Objet = Objet("catapulte.png", 400, 120, 560)
        self.singe: Personnage = Personnage(150, 280, 10)
        self.bananes: pygame.sprite.Group = pygame.sprite.Group()
        self.pilliers: list[pygame.Rect] = []

        self.nb_objets: int = 3
        for i in range(self.nb_objets):
            rectangle = pygame.Rect(500 + i * 120, 0, 80, 200 + i * 100)
            rectangle.bottom = 550
            self.pilliers.append(rectangle)
            self.bananes.add(
                Objet("banane.png", 30, rectangle.centerx, rectangle.top - 5)
            )

        self.vies = 5
        self.points = 0

        self.largeur = largeur
        self.hauteur = hauteur

    def affiche_scene(self, fenetre: pygame.Surface) -> None:
        """Affiche les éléments du jeu"""
        vert = pygame.Color(33, 73, 59)
        noir = pygame.Color(0, 0, 0)

        fenetre.blit(self.decors.image, self.decors.rect)
        for rectangle in self.pilliers:
            pygame.draw.rect(fenetre, vert, rectangle)
            pygame.draw.rect(fenetre, noir, rectangle, 1)
        self.bananes.draw(fenetre)
        fenetre.blit(self.catapulte.image, self.catapulte.rect)
        fenetre.blit(self.singe.image, self.singe.rect)

    def joue_tour(self) -> None:
        """Joue un tour du jeu"""
        # déplacements du songe
        self.singe.deplace_personnage()

        # collision avec une banane
        if pygame.sprite.spritecollide(self.singe, self.bananes, True):
            self.points += 1

        # fin de catapultage
        if self.singe.sort_fenetre(self.largeur, self.hauteur):
            self.singe.revient_depart()
            self.vies -= 1

    def passe_suivant(self) -> bool:
        """et renvoie si la partie est terminée"""
        return self.perdu or self.gagne

    @property
    def perdu(self) -> bool:
        """partie perdue"""
        return self.vies == 0

    @property
    def gagne(self) -> bool:
        """partie gagnée"""
        return self.points == self.nb_objets


class Fin:
    """Scène de fin"""

    # TODO distinguer victoire/défaite

    def __init__(self, largeur: int, hauteur: int) -> None:
        self.fond_fin: Fond = Fond("jungle.png", largeur, hauteur)
        self.message_gagne: Message = Message("Gagné !", "Avdira.otf", 100)
        self.rejouer: Bouton = Bouton(Message("Rejouer", "Avdira.otf", 50))
        self.hauteur: int = hauteur

    def affiche_scene(self, fenetre: pygame.Surface) -> None:
        """Affiche la scène de fin"""
        blanc = pygame.Color(255, 255, 255)
        jaune = pygame.Color(255, 255, 0)
        noir = pygame.Color(0, 0, 0)

        fenetre.blit(self.fond_fin.image, self.fond_fin.rect)
        self.message_gagne.affiche(fenetre, blanc, self.hauteur // 2, 150)
        couleur = jaune if self.rejouer.touche_souris() else blanc
        self.rejouer.affiche(fenetre, couleur, noir, self.hauteur // 2, 400)

    def joue_tour(self) -> None:
        """Joue un tour de jeu"""

    def passe_suivant(self) -> bool:
        """Vérifie si le bouton rejouer est cliqué"""
        return self.rejouer.est_clique()
