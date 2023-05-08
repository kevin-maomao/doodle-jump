import pygame
import random
from .constants import *
from .sprites.platform import Platform


def game_over(surf, clock, assets, all_sprites, doodle, score):
    drop, target_pos = HEIGHT * 2, HEIGHT // 3
    camera_y = drop + target_pos

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        all_sprites.update()
        if camera_y > target_pos:
            for sprite in all_sprites:
                sprite.rect.y -= GG_SPEED
            camera_y -= GG_SPEED
        else:
            doodle.rect.y -= GG_SPEED

        surf.blit(assets["background"], (0, 0))
        all_sprites.draw(surf)
        draw_text(
            surf, assets["font"],
            f"Your score: {score}",
            32, BLACK, HALF_WIDTH, camera_y, centerx=True
        )
        pygame.display.update()


def draw_text(surf, font_name, text, size, color, x, y, centerx=False):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if centerx:
        text_rect.centerx = x
    else:
        text_rect.x = x
    text_rect.y = y
    surf.blit(text_surface, text_rect)


def generate_init_platform(assets, sprites, y):
    space = WIDTH / 9
    for i in range(5):
        platform = Platform(assets["green_pf"], (0, HEIGHT), "green")
        platform.rect.x = i * space * 2
        platform.rect.y = y
        for sprite in sprites:
            sprite.add(platform)


def generate_platform(assets, sprites, y_range, difficulty):
    if difficulty > 1:
        if random.random() > 0.9 or difficulty == 5:
            blue_prob = 1.
        else:
            blue_prob = BLUE_PROB
    else:
        blue_prob = 0.

    if difficulty > 4:
        difficulty = random.randint(2, 4)

    platforms = {"green": assets["green_pf"], "blue": assets["blue_pf"]}

    for i in range(y_range[0], y_range[1], -100):
        min_i = max(i-100, y_range[1])
        for _ in range(5 - difficulty):
            if random.random() > blue_prob:
                pf = "green"
            else:
                pf = "blue"
            platform = Platform(platforms[pf], (min_i, i), pf)
            for sprite in sprites:
                sprite.add(platform)
