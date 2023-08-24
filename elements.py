"""
Contient les éléments du jeu: Personnages, objets, fonds
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
            "singe.png"
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


class Objet(pygame.sprite.Sprite):
    """Objet à attrapper
    filename: fichier contenant l'image
    centerx_depart, bottomy_depart: position initiale de l'objet
    largeur_objet: largeur de l'objet
    """

    def __init__(
        self,
        filename: str,
        centerx_depart: int,
        bottomy_depart: int,
        largeur_objet: int,
    ) -> None:
        super().__init__()

        self.image: pygame.Surface = pygame.image.load(
            filename
        ).convert_alpha()
        self.image = pygame.transform.scale_by(
            self.image, largeur_objet / self.image.get_width()
        )

        self.rect: pygame.Rect = self.image.get_rect(
            midbottom=(centerx_depart, bottomy_depart)
        )


class Vies:
    """Gestion des vies"""

    def __init__(self, vies_max: int) -> None:
        self.vies: int = vies_max
        self.image = pygame.image.load("heart.png").convert_alpha()
        self.image = pygame.transform.scale_by(
            self.image, 30 / self.image.get_width()
        )

    def perd(self, nombre: int) -> None:
        """Perd des vies"""
        self.vies -= nombre

    def affiche(self, x: int, y: int) -> None:
        """Affiche les vies"""
        fenetre = pygame.display.get_surface()
        for i in range(self.vies):
            fenetre.blit(self.image, (x + i * (self.image.get_width() + 5), y))

    @property
    def mort(self) -> bool:
        """Détermine si le personnage est mort"""
        return self.vies == 0
