"""
Gestion du texte et des boutons
"""

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
        self, couleur: pygame.Color, centerx: int, centery: int
    ):
        """Génère le message"""
        self.surface = self.police.render(self.texte, True, couleur)
        self.rect = self.surface.get_rect(center=(centerx, centery))

    def affiche(
        self,
        couleur: pygame.Color,
        centerx: int,
        centery: int,
    ) -> None:
        """Affiche le message sur la fenêtre"""
        fenetre = pygame.display.get_surface()
        self.genere_surface(couleur, centerx, centery)
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
        couleur: pygame.Color,
        couleur_fond: pygame.Color,
        centerx: int,
        centery: int,
    ) -> None:
        """Affiche le message sur la fenêtre"""
        fenetre = pygame.display.get_surface()
        self.message.genere_surface(couleur, centerx, centery)
        self.bouton = self.message.rect.inflate(15, 15)
        self.bouton.center = (centerx, centery)
        pygame.draw.rect(fenetre, couleur_fond, self.bouton, border_radius=20)
        self.message.affiche(couleur, centerx, centery)

    def touche_souris(self) -> bool:
        """Détermine si la souris touche le bouton"""
        return self.bouton.collidepoint(pygame.mouse.get_pos())

    def est_clique(self) -> bool:
        """Détermine si on clique sur le bouton"""
        return self.touche_souris() and pygame.mouse.get_pressed()[0]
