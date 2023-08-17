"""
Gestion du texte et des boutons
"""

# TODO update

import pygame


class Message:
    """Message
    texte: texte à afficher
    nom_police: nom du fichier de police pour afficher le message
    taille: taille du texte
    """

    def __init__(self, texte: str, nom_police: str, taille: int) -> None:
        self.police: pygame.font.Font = pygame.font.Font(nom_police, taille)
        self.texte: str = texte
        self.surface: pygame.Surface = pygame.Surface((0, 0))
        self.rect: pygame.Rect = self.surface.get_rect()

    def genere_surface(
        self, couleur: pygame.Color, x_center: int, y_center: int
    ):
        """Génère le message"""
        self.surface = self.police.render(self.texte, True, couleur)
        self.rect = self.surface.get_rect(center=(x_center, y_center))

    def affiche(
        self,
        fenetre: pygame.Surface,
        couleur: pygame.Color,
        x_center: int,
        y_center: int,
    ) -> None:
        """Affiche le message sur la fenêtre"""
        self.genere_surface(couleur, x_center, y_center)
        fenetre.blit(self.surface, self.rect)


class Bouton:
    """Bouton
    message: texte du bouton
    """

    def __init__(self, message: Message) -> None:
        self.message: Message = message
        self.bouton: pygame.Rect = pygame.Rect(0, 0, 0, 0)

    def affiche(
        self,
        fenetre: pygame.Surface,
        couleur: pygame.Color,
        couleur_fond: pygame.Color,
        x_center: int,
        y_center: int,
    ) -> None:
        """Affiche le message sur la fenêtre"""
        self.message.genere_surface(couleur, x_center, y_center)
        self.bouton = self.message.rect.inflate(15, 15)
        self.bouton.center = (x_center, y_center)
        pygame.draw.rect(fenetre, couleur_fond, self.bouton, border_radius=20)
        self.message.affiche(fenetre, couleur, x_center, y_center)

    def touche_souris(self) -> bool:
        """Détermine si la souris touche le bouton"""
        return self.bouton.collidepoint(pygame.mouse.get_pos())

    def est_clique(self) -> bool:
        """Détermine si on clique sur le bouton"""
        return self.touche_souris() and any(
            evenement.type == pygame.MOUSEBUTTONDOWN
            for evenement in pygame.event.get()
        )
