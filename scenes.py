"""
Gestion des scènes du jeu
"""

from typing import Protocol

import pygame

from elements import Objet, Personnage, Vies
from texte import Bouton, Message


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

        self.decors: Objet = Objet(
            "images/jungle.png", largeur // 2, hauteur, largeur
        )
        self.catapulte: Objet = Objet("images/catapulte.png", 120, 560, 400)
        self.singe: Personnage = Personnage(150, 280, 40, 10)
        self.bananes: pygame.sprite.Group = pygame.sprite.Group()
        self.pilliers: list[pygame.Rect] = []

        self.nb_objets: int = 3
        for i in range(self.nb_objets):
            rectangle = pygame.Rect(500 + i * 120, 0, 80, 200 + i * 100)
            rectangle.bottom = 550
            self.pilliers.append(rectangle)
            self.bananes.add(
                Objet(
                    "images/banane.png",
                    rectangle.centerx,
                    rectangle.top - 5,
                    30,
                )
            )

        self.points: int = 0
        self.vies: Vies = Vies(5)

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
        self.vies.affiche(20, 20)

    def joue_tour(self) -> None:
        """Joue un tour du jeu"""
        # déplacements du songe
        self.singe.deplace_personnage()

        # collision avec une banane
        if pygame.sprite.spritecollide(self.singe, self.bananes, True):
            self.points += 1

        # fin de catapultage
        if self.singe.sort_fenetre():
            self.singe.revient_depart()
            self.vies.perd(1)

    def passe_suivant(self) -> bool:
        """Renvoie si la partie est terminée"""
        return self.perdu or self.gagne

    @property
    def perdu(self) -> bool:
        """Partie perdue"""
        return self.vies.mort

    @property
    def gagne(self) -> bool:
        """Partie gagnée"""
        return self.points == self.nb_objets


class Fin:
    """Scène de fin"""

    def __init__(self, victoire: bool) -> None:
        largeur, hauteur = pygame.display.get_window_size()

        self.decors: Objet = Objet(
            "images/jungle.png", largeur // 2, hauteur, largeur
        )
        self.message_fin: Message = (
            Message("Gagné !", "font/Avdira.otf", 100)
            if victoire
            else Message("Perdu ...", "font/Avdira.otf", 100)
        )
        self.bouton_rejouer: Bouton = Bouton(
            Message("Rejouer", "font/Avdira.otf", 50)
        )

    def affiche_scene(self) -> None:
        """Affiche la scène de fin"""
        fenetre = pygame.display.get_surface()
        largeur, _ = pygame.display.get_window_size()

        fenetre.blit(self.decors.image, self.decors.rect)
        couleur_message = pygame.Color(255, 255, 255)
        self.message_fin.affiche(couleur_message, largeur // 2, 150)
        couleur_texte = (
            pygame.Color(101, 172, 171)
            if self.bouton_rejouer.touche_souris()
            else pygame.Color(240, 240, 240)
        )
        couleur_fond = (
            pygame.Color(80, 80, 80)
            if self.bouton_rejouer.touche_souris()
            else pygame.Color(50, 50, 50)
        )
        self.bouton_rejouer.affiche(
            couleur_texte, couleur_fond, largeur // 2, 400
        )

    def joue_tour(self) -> None:
        """Rien"""

    def passe_suivant(self) -> bool:
        """Vérifie si le bouton rejouer est cliqué"""
        return self.bouton_rejouer.est_clique()
