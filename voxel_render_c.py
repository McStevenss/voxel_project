import pygame as pg
import numpy as np
import math
import matplotlib.pyplot as plt
from noise import pnoise2, snoise2
import cv2
from ray_casting_wrapper import call_ray_casting
from numba import njit
from settings import GAME_SETTINGS
# Generate heightmap using Perlin noise
def generate_heightmap(shape, scale, octaves, persistence, lacunarity):
    heightmap = np.zeros((shape[0],shape[1],3))
    for i in range(shape[0]):
        for j in range(shape[1]):
            heightmap[i][j] = pnoise2(i / scale, 
                                      j / scale, 
                                      octaves=octaves, 
                                      persistence=persistence, 
                                      lacunarity=lacunarity, 
                                      repeatx=shape[0], 
                                      repeaty=shape[1], 
                                      base=0)
            
    normalized_heightmap = (heightmap - np.min(heightmap)) / (np.max(heightmap) - np.min(heightmap))
    image_array = np.uint8(normalized_heightmap * 255)
    return image_array

# Function to map height to color using numpy vectorized operations
def generate_colormap(heightmap):
    # Create an empty color image with 3 channels for RGB
    color_image = np.zeros((heightmap.shape[0], heightmap.shape[1], 3), dtype=np.uint8)

    # Map heights [0, 85) to blue (0, 0, 255)

    mask = heightmap < 50

    color_image[mask[..., 0], 0] = 0  # Red channel
    color_image[mask[..., 1], 1] = 0  # Green channel
    color_image[mask[..., 2], 2] = 150  # Blue channel


    mask = (heightmap >=50) & (heightmap < 85)
    #color_image[mask] = [0, 0, 255] 

    color_image[mask[..., 0], 0] = 0  # Red channel
    color_image[mask[..., 1], 1] = 0  # Green channel
    color_image[mask[..., 2], 2] = 255  # Blue channel

    mask = (heightmap >= 85) & (heightmap < 95)
    
    color_image[mask[..., 0], 0] = 255  # Red channel
    color_image[mask[..., 1], 1] = 244  # Green channel
    color_image[mask[..., 2], 2] = 5  # Blue channel

    # Map heights [85, 170) to green (0, 255, 0)
    mask = (heightmap >= 95) & (heightmap < 130)
    #color_image[mask] = [0, 255, 0]
    color_image[mask[..., 0], 0] = 0  # Red channel
    color_image[mask[..., 1], 1] = 200  # Green channel
    color_image[mask[..., 2], 2] = 0  # Blue channel

    # Map heights [85, 170) to green (0, 255, 0)
    mask = (heightmap >= 130) & (heightmap < 200)
    #color_image[mask] = [0, 255, 0]
    color_image[mask[..., 0], 0] = 0  # Red channel
    color_image[mask[..., 1], 1] = 255  # Green channel
    color_image[mask[..., 2], 2] = 0  # Blue channel

    # Map heights [170, 255] to white (255, 255, 255)
    mask = heightmap >= 200
    #color_image[mask] = [255, 255, 255]
    color_image[mask[..., 0], 0] = 255  # Red channel
    color_image[mask[..., 1], 1] = 255  # Green channel
    color_image[mask[..., 2], 2] = 255  # Blue channel

    return color_image

height_map_img = pg.image.load(GAME_SETTINGS["height_map"])
height_map = pg.surfarray.array3d(height_map_img)

color_map_img = pg.image.load(GAME_SETTINGS["color_map"])
color_map = pg.surfarray.array3d(color_map_img)

# Parameters for the heightmap
# shape = (1024*4, 1024*4)         # Size of the heightmap
# scale = 100.0              # Scale of the noise
# octaves = 6                # Number of octaves
# persistence = 0.1          # Persistence of the noise
# lacunarity = 2.0           # Lacunarity of the noise

# gen_heightmap = generate_heightmap(shape, scale, octaves, persistence, lacunarity)
# color_map = generate_colormap(gen_heightmap)

map_height = len(height_map[0])
map_width = len(height_map)


@njit(fastmath=True)
def ray_casting(screen_array, player_pos, player_angle, player_height, player_pitch,
                screen_width, screen_height, delta_angle, ray_distance, h_fov, scale_height,
                height_map, color_map, map_width, map_height):

    screen_array[:] = np.array([119, 241, 255], dtype=np.uint8)
    y_buffer = np.full(screen_width, screen_height, dtype=np.int32)

    ray_angles = player_angle - h_fov + delta_angle * np.arange(screen_width)
    sin_a = np.sin(ray_angles)
    cos_a = np.cos(ray_angles)

    for num_ray in range(screen_width):
        first_contact = False
        for depth in range(1, ray_distance):
            x = int(player_pos[0] + depth * cos_a[num_ray])
            y = int(player_pos[1] + depth * sin_a[num_ray])

            if 0 < x < map_width and 0 < y < map_height:
                depth_corrected = depth * math.cos(player_angle - ray_angles[num_ray])
                height_on_screen = int((player_height - height_map[x, y, 0]) / depth_corrected * scale_height + player_pitch)

                if not first_contact:
                    y_buffer[num_ray] = min(height_on_screen, screen_height)
                    first_contact = True

                if height_on_screen < 0:
                    height_on_screen = 0

                if height_on_screen < y_buffer[num_ray]:
                    for screen_y in range(height_on_screen, y_buffer[num_ray]):
                        screen_array[num_ray, screen_y] = color_map[x, y]
                    y_buffer[num_ray] = height_on_screen

    return screen_array


class VoxelRender:
    def __init__(self, app):
        self.app = app
        self.player = app.player
        self.fov = GAME_SETTINGS["fov"]
        self.h_fov = self.fov / 2
        self.num_rays = app.width
        self.delta_angle = self.fov / self.num_rays
        self.ray_distance = GAME_SETTINGS["render_distance"]
        self.scale_height = GAME_SETTINGS["height_scale"]
        self.screen_array = np.full((app.width, app.height, 3), GAME_SETTINGS["sky_color"], dtype=np.uint8)

    def update(self):
        if not self.player.is_flying:
            self.player.height = height_map[int(self.player.pos[0]) % map_width, int(self.player.pos[1]) % map_height][0] + self.player.player_height

        # C function!
        call_ray_casting(self.screen_array, self.player.pos, self.player.angle,
                        self.player.height, self.player.pitch, self.app.width,
                        self.app.height, self.delta_angle, self.ray_distance,
                        self.h_fov, self.scale_height,
                        height_map, color_map, map_width, map_height)


    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

