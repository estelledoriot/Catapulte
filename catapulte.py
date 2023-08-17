"""Jeu de catapulte
    - tourne le personnage en utilisant les flèches directionnelles
    - appuie sur la touche espace pour catapulter le personnage
    - attrape toutes les bananes pour gagner
    - tu as 5 essais maximum pour réussir
"""

# TODO: ajout sons

import pygame

from scenes import Fin, Partie, Scene


class Fenetre:
    """Jeu"""

    def __init__(self) -> None:
        pygame.init()

        # fenêtre
        self.largeur: int = 850
        self.hauteur: int = 565
        self.fenetre: pygame.Surface = pygame.display.set_mode(
            (self.largeur, self.hauteur)
        )
        pygame.display.set_caption("Catapulte")
        pygame.display.set_icon(pygame.image.load("catapult.png"))

        # état
        self.scenes: list = [Partie, Fin]
        self.scene_courante: Scene = Partie(self.largeur, self.hauteur)
        self.no_scene: int = 0
        self.clock: pygame.time.Clock = pygame.time.Clock()

    def scene_suivante(self):
        """Passe à la scène suivante"""
        self.no_scene += 1
        self.scene_courante = self.scenes[self.no_scene % 2](
            self.largeur, self.hauteur
        )

    def jouer(self) -> None:
        """Lance le jeu"""
        while True:
            self.scene_courante.joue_tour()
            if self.scene_courante.passe_suivant():
                self.scene_suivante()

            # quitter
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    return

            # affichage
            self.scene_courante.affiche_scene(self.fenetre)
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    jeu = Fenetre()
    jeu.jouer()
    pygame.quit()
