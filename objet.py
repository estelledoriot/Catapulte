"""
Contient les éléments du jeu: Personnages, objets, vies
"""


import pygame


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
