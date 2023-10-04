"""
Gestion des scènes du jeu
"""

from enum import Enum

import pygame

from button import Button
from lives import Lives
from monkey import Monkey
from object import Object
from text import Text

Stage = Enum("Stage", ["RUNNING", "END", "TERMINATE"])


class Game:
    """Une partie de labyrinthe"""

    def __init__(self, width: int, height: int) -> None:
        # décors
        self.background: Object = Object(
            "images/jungle.png", (width // 2, height), width
        )

        # game elements
        self.catapulte: Object = Object(
            "images/catapulte.png", (120, 560), 400
        )
        self.monkey: Monkey = Monkey((150, 280), 40, 10)
        self.bananas: pygame.sprite.Group = pygame.sprite.Group()
        self.pillars: list[pygame.Rect] = []

        self.nb_objets: int = 3
        for i in range(self.nb_objets):
            rectangle = pygame.Rect(500 + i * 120, 0, 80, 200 + i * 100)
            rectangle.bottom = 550
            self.pillars.append(rectangle)
            self.bananas.add(
                Object(
                    "images/banane.png",
                    (rectangle.centerx, rectangle.top - 5),
                    30,
                )
            )
        self.points: int = 0
        self.lives: Lives = Lives(5, (20, 20))
        self.game_elements: pygame.sprite.Group = pygame.sprite.Group()
        self.game_elements.add(
            self.background,
            self.catapulte,
            self.monkey,
            self.bananas,
            self.lives,
        )

        # end elements
        self.end_message: Text = Text("", (width // 2, 150))
        self.restart_button: Button = Button(
            "Rejouer", (250, 80), (width // 2, 400)
        )
        self.end_elements: pygame.sprite.Group = pygame.sprite.Group()
        self.end_elements.add(
            self.background, self.end_message, self.restart_button
        )

        # sons
        self.collision_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/Glug.wav"
        )
        self.collision_sound.set_volume(0.25)
        self.win_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/win.wav"
        )
        self.win_sound.set_volume(0.25)
        self.lose_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/lose.mp3"
        )
        self.lose_sound.set_volume(0.5)
        self.button_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/pop.wav"
        )
        self.button_sound.set_volume(0.25)

        # stage
        self.stage: Stage = Stage.RUNNING

    @property
    def won(self) -> bool:
        """Vérifie si la partie est gagnée (le personnage touche la pokeball)"""
        return self.points == self.nb_objets

    @property
    def lost(self) -> bool:
        """Vérifie si la partie est perdue (le temps est écoulé)"""
        return self.lives.is_dead

    def run_game(self) -> None:
        """Fait tourner le jeu"""
        largeur, hauteur = pygame.display.get_window_size()
        # mise à jour des éléments du jeu
        self.game_elements.update()

        # collision avec une banane
        if pygame.sprite.spritecollide(self.monkey, self.bananas, True):
            self.collision_sound.play()
            self.points += 1

        # fin de catapultage
        if self.monkey.is_out_screen(largeur, hauteur):
            self.monkey.goto_start()
            self.lives.lose(1)

        # fin du jeu
        if self.won or self.lost:
            self.stage = Stage.END
            self.end_message.update_text(
                "Gagné !" if self.won else "Perdu ..."
            )
            if self.won:
                self.win_sound.play()
            else:
                self.lose_sound.play()

    def draw_game(self, screen: pygame.Surface) -> None:
        """Affiche les éléments du jeu"""
        self.game_elements.draw(screen)

        couleur_pilliers = pygame.Color(33, 73, 59)
        couleur_bordure = pygame.Color(0, 0, 0)
        for rectangle in self.pillars:
            pygame.draw.rect(screen, couleur_pilliers, rectangle)
            pygame.draw.rect(screen, couleur_bordure, rectangle, 1)

        screen.blit(self.monkey.image, self.monkey.rect)

    def run_end(self) -> None:
        """Fait tourner l'écran de fin"""
        # mise à jour des éléments de l'écran de fin
        self.restart_button.update()

        # clic sur le bouton pour commencer une nouvelle partie
        for _ in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if self.restart_button.touch_mouse():
                self.button_sound.play()
                self.stage = Stage.TERMINATE

    def draw_end(self, screen: pygame.Surface) -> None:
        """Affiche les éléments de l'écran de fin"""
        self.end_elements.draw(screen)
