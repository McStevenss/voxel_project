import pygame as pg
import numpy as np
import math
import matplotlib.pyplot as plt
from noise import pnoise2, snoise2
import cv2
from ray_casting_wrapper import call_ray_casting
from numba import njit
from settings import GAME_SETTINGS


class VoxelRender:
    def __init__(self, app):
        self.app = app
        self.player = app.player
        self.fov = GAME_SETTINGS["fov"]
        self.h_fov = self.fov / 2
        self.num_rays = app.width
        self.delta_angle = self.fov / self.num_rays

        print(f"Rays: {self.num_rays}, delta angle: {self.delta_angle}")

        self.ray_distance = GAME_SETTINGS["render_distance"]
        self.scale_height = GAME_SETTINGS["height_scale"]
        self.screen_array = np.full((app.width, app.height, 3), GAME_SETTINGS["sky_color"], dtype=np.uint8)

        self.height_map_img = pg.image.load(GAME_SETTINGS["height_map"])
        self.height_map = pg.surfarray.array3d(self.height_map_img)
        self.color_map_img = pg.image.load(GAME_SETTINGS["color_map"])
        self.color_map = pg.surfarray.array3d(self.color_map_img)

        self.map_height = len(self.height_map[0])
        self.map_width = len(self.height_map)



    def draw_sprites(self, screen_array, sprites):
        for sprite in sprites:
            size = sprite.size
            half_size = size // 2
            screen_x = sprite.screen_x - half_size
            screen_y = sprite.screen_y - half_size

            # Ensure the sprite is within screen bounds
            x_start = max(screen_x, 0)
            y_start = max(screen_y, 0)
            x_end = min(screen_x + size, screen_array.shape[1])
            y_end = min(screen_y + size, screen_array.shape[0])

            texture = sprite.texture

            for x in range(x_start, x_end):
                for y in range(y_start, y_end):
                    tex_x = int((x - screen_x) * texture.shape[1] / size)
                    tex_y = int((y - screen_y) * texture.shape[0] / size)

                    # Ensure texture coordinates are within bounds
                    tex_x = max(min(tex_x, texture.shape[1] - 1), 0)
                    tex_y = max(min(tex_y, texture.shape[0] - 1), 0)

                    color = texture[tex_y, tex_x]
                    # Apply alpha blending
                    if len(color) == 4:
                        alpha = color[3] / 255.0
                        screen_color = screen_array[y, x]
                        screen_array[y, x] = [
                            int(screen_color[0] * (1 - alpha) + color[0] * alpha),
                            int(screen_color[1] * (1 - alpha) + color[1] * alpha),
                            int(screen_color[2] * (1 - alpha) + color[2] * alpha)
                        ]
        return screen_array

    def sort_sprites(self, sprites):
        sprites.sort(key=lambda sprite: sprite.distance, reverse=True)

    def update(self):
        if not self.player.is_flying:
            self.player.height = self.height_map[int(self.player.pos[0]) % self.map_width, int(self.player.pos[1]) % self.map_height][0] + self.player.player_height

        # C function!
        call_ray_casting(self.screen_array, self.player.pos, self.player.angle,
                        self.player.height, self.player.pitch, self.app.width,
                        self.app.height, self.delta_angle, self.ray_distance,
                        self.h_fov, self.scale_height,
                        self.height_map, self.color_map, self.map_width, self.map_height,fog_color=(119, 241, 255),fog_density=0.001)


#    def draw(self):
#        pg.surfarray.blit_array(self.app.screen, self.screen_array)


    def draw(self):
        # Draw the voxel space first
        pg.surfarray.blit_array(self.app.screen, self.screen_array)
