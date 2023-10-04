"""
classe Monkey
"""

from math import cos, radians, sin

import pygame


class Monkey(pygame.sprite.Sprite):
    """Personnage du jeu
    Peut tourner sur lui même et être catapulté
    start_center: position initiale du personnage
    width: taille du personnage
    speed: vitesse de déplacement du personnage
    """

    def __init__(
        self,
        start_center: tuple[int, int],
        width: int,
        speed: int,
    ) -> None:
        super().__init__()

        # image
        self.initial_image: pygame.Surface = pygame.image.load(
            "images/singe.png"
        ).convert_alpha()
        self.initial_image = pygame.transform.scale_by(
            self.initial_image, width / self.initial_image.get_width()
        )
        self.image: pygame.Surface = self.initial_image

        # position
        self.start_position: tuple[int, int] = start_center
        self.rect: pygame.Rect = self.image.get_rect()
        self.goto_start()

        self.direction: int = 0
        self.speed: int = speed
        self.is_moving: bool = False

    def is_out_screen(self, width: int, height: int) -> bool:
        """Vérifie si le personnage sort de la fenêtre"""
        return (
            self.rect.left < 0
            or self.rect.right > width
            or self.rect.top < 0
            or self.rect.bottom > height
        )

    def goto_start(self) -> None:
        """Replace le personnage à son point de départ"""
        self.direction = 0
        self.image = self.initial_image
        self.rect = self.initial_image.get_rect()
        self.rect.center = self.start_position
        self.is_moving = False

    def rotate(self, angle: int) -> None:
        """Fait tourner le personnage"""
        center = self.rect.center
        self.direction += angle
        self.image = pygame.transform.rotate(
            self.initial_image, self.direction
        )
        self.rect = self.image.get_rect()
        self.rect.center = center

    def move(self) -> None:
        """Fait avancer le personnage"""
        self.rect.x += int(self.speed * cos(radians(self.direction)))
        self.rect.y -= int(self.speed * sin(radians(self.direction)))

    def update(self) -> None:
        """Déplacement du personnage suivant les touches pressées"""
        if self.is_moving:
            self.move()
        else:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RIGHT]:
                self.rotate(-1)
            elif pressed[pygame.K_LEFT]:
                self.rotate(1)
            elif pressed[pygame.K_SPACE]:
                self.is_moving = True
