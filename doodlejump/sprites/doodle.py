import pygame
from typing import Any, Union
from ..constants import *


class Doodle(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.images = [image, pygame.transform.flip(image, True, False)]

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.layer = 10

        self.rect.center = (HALF_WIDTH, HEIGHT*2//3)

        self.speed_x = MOV_SPEED
        self.speed_y = 0

        self.acce_y = GRAVITY
        self.jump_speed = -JUMP_SPEED

        self.direction = 0

    def update(self):
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_RIGHT]:
            self.flip_lr(0)
            self.rect.x += self.speed_x
        if key_pressed[pygame.K_LEFT]:
            self.flip_lr(1)
            self.rect.x -= self.speed_x

        self.speed_y += self.acce_y
        self.rect.y += round(self.speed_y)

        if self.rect.centerx < 0:
            self.rect.centerx = WIDTH
        if self.rect.centerx > WIDTH:
            self.rect.centerx = 0

    def jump(self):
        self.speed_y = self.jump_speed

    def jump_spring(self):
        self.speed_y = self.jump_speed * 1.5

    def shoot(self, img_bullet: pygame.Surface, sprites: list[Union[pygame.sprite.Group, Any]]):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top)
        for sprite in sprites:
            sprite.add(bullet)

    def flip_lr(self, flip_direction: int):
        if flip_direction != self.direction:
            self.direction = flip_direction
            self.image = self.images[self.direction]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        self.layer = 9

        self.speed_y = -BULLET_SPEED

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()
