"""Jeu de catapulte
    - tourne le personnage en utilisant les flèches directionnelles
    - appuie sur la touche espace pour catapulter le personnage
    - attrape toutes les bananes pour gagner
    - tu as 5 essais maximum pour réussir
"""

import pygame

from game import Game, Stage


class Catapulte:
    """Jeu"""

    def __init__(self) -> None:
        pygame.init()

        # fenêtre
        self.width: int = 850
        self.height: int = 565
        self.screen: pygame.Surface = pygame.display.set_mode(
            (self.width, self.height)
        )
        pygame.display.set_caption("Catapulte")
        pygame.display.set_icon(pygame.image.load("images/catapult.png"))

        # état
        self.game: Game = Game(self.width, self.height)
        self.clock: pygame.time.Clock = pygame.time.Clock()

    def run(self) -> None:
        """Lance le jeu"""
        while True:
            if self.game.stage == Stage.TERMINATE:
                self.game = Game(self.width, self.height)

            if self.game.stage == Stage.RUNNING:
                self.game.run_game()
                self.game.draw_game(self.screen)

            if self.game.stage == Stage.END:
                self.game.run_end()
                self.game.draw_end(self.screen)

            # quitter
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    return

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    jeu = Catapulte()
    jeu.run()
    pygame.quit()
