import pygame
import os
from .constants import *
from .sprites.doodle import Doodle
from .pages.game_over import game_over
from .pages.menu import menu
from .pages.pause import pause
from .generate import (
    generate_platform,
    generate_init_platform,
    draw_text
)
from .collide import jump_platform


def load_assets(assets_root):
    assets = dict()
    assets["background"] = pygame.image.load(os.path.join(assets_root, "background.png")).convert()
    assets["transparent_bg"] = assets["background"].copy()
    assets["transparent_bg"].set_alpha(200)
    assets["green_pf"] = pygame.image.load(os.path.join(assets_root, "platforms", "green.png")).convert_alpha()
    assets["blue_pf"] = pygame.image.load(os.path.join(assets_root, "platforms", "blue.png")).convert_alpha()
    assets["doodle"] = pygame.image.load(os.path.join(assets_root, "doodle.png")).convert_alpha()
    assets["button"] = pygame.image.load(os.path.join(assets_root, "buttons", "button.png")).convert_alpha()
    assets["selected_button"] = pygame.image.load(os.path.join(
        assets_root, "buttons", "selected_button.png")).convert_alpha()
    assets["spring"] = pygame.image.load(os.path.join(assets_root, "springs", "spring.png")).convert_alpha()
    assets["compressed_spring"] = pygame.image.load(os.path.join(
        assets_root, "springs", "compressed_spring.png")).convert_alpha()
    assets["bullet"] = pygame.image.load(os.path.join(assets_root, "bullet.png")).convert_alpha()

    assets["font"] = os.path.join(assets_root, "Gochi_Hand", "GochiHand-Regular.ttf")

    return assets


class Game:
    def __init__(self, assets_root="./doodlejump/assets/"):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Doodle Jump")
        self.clock = pygame.time.Clock()

        self.assets = load_assets(assets_root)

        # initial settings
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platform_sprites = pygame.sprite.Group()
        self.doodle = Doodle(self.assets["doodle"])

        self.camera_move = 0
        self.stage = 1
        self.score = 0
        self.running = True
        self.gameover = False
        self.showmenu = False

    def init_game(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platform_sprites = pygame.sprite.Group()

        self.doodle = Doodle(self.assets["doodle"])
        self.all_sprites.add(self.doodle)

        generate_init_platform(self.assets, [self.all_sprites, self.platform_sprites], HEIGHT-50)
        generate_platform(
            self.assets,
            [self.all_sprites, self.platform_sprites],
            (HEIGHT-100, -STAGE_LENGTH-BUFFER_LENGTH),
            1
        )

        self.camera_move = 0
        self.stage = 1
        self.score = 0
        self.running = True
        self.gameover = False
        self.showmenu = False

    def run(self):
        self.showmenu = True

        while self.running:
            if self.gameover:
                close = game_over(
                    self.screen,
                    self.clock,
                    self.assets,
                    self.all_sprites,
                    self.doodle,
                    self.score
                )
                self.gameover = False
                if close == 0:
                    self.init_game()
                elif close == 1:
                    self.showmenu = True
                elif close == -1 or close == 2:
                    break
                else:
                    raise ValueError("Unexpected value of [close]")

            if self.showmenu:
                close = menu(self.screen, self.clock, self.assets)
                if close == 0:
                    self.init_game()
                elif close == -1 or close == 1:
                    break
                else:
                    raise ValueError("Unexpected value of [close]")

            self.clock.tick(FPS)

        # get inputs
            flag = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        close = pause(self.screen, self.clock, self.assets, self.all_sprites, self.score)
                        if close == 0:
                            pass
                        elif close == 1:
                            self.showmenu = True
                        elif close == -1:
                            flag = True
                        else:
                            raise ValueError("Unexpected value of [close]")
                    elif event.key == pygame.K_SPACE:
                        self.doodle.shoot(self.assets["bullet"], [self.all_sprites])
            if flag:
                break

        # update game
            self.all_sprites.update()
            jump_platform(self.doodle, self.platform_sprites)

            # move camera
            if self.doodle.rect.y < HALF_HEIGHT:
                diff = HALF_HEIGHT - self.doodle.rect.y
                self.camera_move += diff
                self.score += diff
                for sprite in self.all_sprites:
                    sprite.rect.y += diff
                if self.camera_move > STAGE_LENGTH:
                    self.stage += 1
                    bot = self.camera_move-STAGE_LENGTH-BUFFER_LENGTH
                    generate_platform(
                        self.assets,
                        [self.all_sprites, self.platform_sprites],
                        (bot, bot-STAGE_LENGTH),
                        self.stage
                    )
                    self.camera_move = 0

            if self.doodle.rect.y > HEIGHT:
                self.gameover = True

        # display
            self.screen.blit(self.assets["background"], (0, 0))
            self.all_sprites.draw(self.screen)
            draw_text(self.screen, self.assets["font"], str(self.score), 32, BLACK, 10, 0)
            pygame.display.update()

        pygame.quit()
