"""
Contient les éléments du jeu: Personnages, objets, fonds
"""

from math import cos, radians, sin

import pygame


class Personnage(pygame.sprite.Sprite):
    """Personnage du jeu
    Peut tourner sur lui même et être catapulté
    centerx_depart, centery_depart: position initiale du personnage
    vitesse: vitesse de déplacement du personnage
    """

    def __init__(
        self, centerx_depart: int, centery_depart: int, vitesse: int
    ) -> None:
        super().__init__()

        self.vitesse: int = vitesse
        self.en_mouvement: bool = False

        self.image_initiale: pygame.Surface = pygame.image.load("singe.png")
        self.image_initiale = pygame.transform.scale_by(
            self.image_initiale, 40 / self.image_initiale.get_width()
        )
        self.image: pygame.Surface = self.image_initiale

        self.centerx_depart: int = centerx_depart
        self.centery_depart: int = centery_depart
        self.rect: pygame.Rect = self.image.get_rect()
        self.direction: int = 0
        self.revient_depart()

    def deplace_personnage(self) -> None:
        """Déplacement du personnage suivant les touches pressées"""
        if self.en_mouvement:
            self.avance()
        else:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RIGHT]:
                self.tourne(-1)
            elif pressed[pygame.K_LEFT]:
                self.tourne(1)
            elif pressed[pygame.K_SPACE]:
                self.en_mouvement = True

    def tourne(self, angle: int) -> None:
        """Fait tourner le personnage"""
        center = self.rect.center
        self.direction += angle
        self.image = pygame.transform.rotate(
            self.image_initiale, self.direction
        )
        self.rect = self.image.get_rect()
        self.rect.center = center

    def avance(self) -> None:
        """Fait avancer le personnage"""
        self.rect.x += int(self.vitesse * cos(radians(self.direction)))
        self.rect.y -= int(self.vitesse * sin(radians(self.direction)))

    def sort_fenetre(self, largeur: int, hauteur: int) -> bool:
        """Vérifie si le personnage sort de la fenêtre"""
        return (
            self.rect.x < 0
            or self.rect.x > largeur
            or self.rect.y < 0
            or self.rect.y > hauteur
        )

    def revient_depart(self) -> None:
        """Replace le personnage à son point de départ"""
        self.direction = 0
        self.image = self.image_initiale
        self.rect = self.image_initiale.get_rect()
        self.rect.center = self.centerx_depart, self.centery_depart
        self.en_mouvement = False


class Objet(pygame.sprite.Sprite):
    """Objet à attrapper
    centerx_depart, bottomy_depart: position initiale de l'objet
    """

    def __init__(
        self,
        filename: str,
        largeur: int,
        centerx_depart: int,
        bottomy_depart: int,
    ) -> None:
        super().__init__()

        self.image: pygame.Surface = pygame.image.load(filename)
        self.image = pygame.transform.scale_by(
            self.image, largeur / self.image.get_width()
        )

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.centerx = centerx_depart
        self.rect.bottom = bottomy_depart


class Fond(pygame.sprite.Sprite):
    """Fond d'écran
    filename: nom du fichier contenant l'image de fond
    largeur: largeur de la fenêtre
    hauteur: hauteur de la fenêtre
    """

    def __init__(
        self,
        filename: str,
        largeur: int,
        hauteur: int,
    ) -> None:
        super().__init__()

        self.image: pygame.Surface = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (largeur, hauteur))

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = largeur // 2, hauteur // 2
