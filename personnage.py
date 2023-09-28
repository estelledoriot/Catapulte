"""
classe Personnage
"""

from math import cos, radians, sin

import pygame


class Personnage(pygame.sprite.Sprite):
    """Personnage du jeu
    Peut tourner sur lui même et être catapulté
    centerx_depart, centery_depart: position initiale du personnage
    taille: taille du personnage
    vitesse: vitesse de déplacement du personnage
    """

    def __init__(
        self,
        centerx_depart: int,
        centery_depart: int,
        taille: int,
        vitesse: int,
    ) -> None:
        super().__init__()

        self.vitesse: int = vitesse
        self.en_mouvement: bool = False

        self.image_initiale: pygame.Surface = pygame.image.load(
            "images/singe.png"
        ).convert_alpha()
        self.image_initiale = pygame.transform.scale_by(
            self.image_initiale, taille / self.image_initiale.get_width()
        )
        self.image: pygame.Surface = self.image_initiale

        self.depart: tuple[int, int] = centerx_depart, centery_depart
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

    def sort_fenetre(self) -> bool:
        """Vérifie si le personnage sort de la fenêtre"""
        largeur, hauteur = pygame.display.get_window_size()
        return (
            self.rect.left < 0
            or self.rect.right > largeur
            or self.rect.top < 0
            or self.rect.bottom > hauteur
        )

    def revient_depart(self) -> None:
        """Replace le personnage à son point de départ"""
        self.direction = 0
        self.image = self.image_initiale
        self.rect = self.image_initiale.get_rect()
        self.rect.center = self.depart
        self.en_mouvement = False
