import pygame as pg
from numba import njit
import numpy as np
import math
import matplotlib.pyplot as plt
from noise import pnoise2, snoise2
import cv2


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

height_map_img = pg.image.load('img/height_map.jpg')
# height_map_img = pg.image.load('img/D10_1.png')
# height_map_img = pg.image.load('img/test.png')
height_map = pg.surfarray.array3d(height_map_img)

color_map_img = pg.image.load('img/color_map.jpg')
# color_map_img = pg.image.load('img/C10.png')
color_map = pg.surfarray.array3d(color_map_img)

# Parameters for the heightmap
# shape = (512, 512)         # Size of the heightmap
# shape = (1024, 1024)         # Size of the heightmap
shape = (1024*4, 1024*4)         # Size of the heightmap
scale = 100.0              # Scale of the noise
octaves = 6                # Number of octaves
persistence = 0.1          # Persistence of the noise
lacunarity = 2.0           # Lacunarity of the noise

#gen_heightmap = generate_heightmap(shape, scale, octaves, persistence, lacunarity)

#color_map = generate_colormap(gen_heightmap)

map_height = len(height_map[0])
map_width = len(height_map)



@njit(fastmath=True)
def ray_casting(screen_array, player_pos, player_angle, player_height, player_pitch,
                     screen_width, screen_height, delta_angle, ray_distance, h_fov, scale_height):

    # screen_array[:] = np.array([0, 0, 0])
    screen_array[:] = np.array([119, 241, 255])
    y_buffer = np.full(screen_width, screen_height)

    ray_angle = player_angle - h_fov
    for num_ray in range(screen_width):
        first_contact = False
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        for depth in range(1, ray_distance):
            x = int(player_pos[0] + depth * cos_a)
            if 0 < x < map_width:
                y = int(player_pos[1] + depth * sin_a)
                if 0 < y < map_height:

                    # remove fish eye and get height on screen
                    depth *= math.cos(player_angle - ray_angle)
                    # height_on_screen = int((player_height - height_map[x, y][0]) /
                    #                         depth * scale_height + player_pitch)

                    height_on_screen = int((player_height - height_map[x,y][0]) /
                       depth * scale_height + player_pitch)

                    # remove unnecessary drawing
                    if not first_contact:
                        y_buffer[num_ray] = min(height_on_screen, screen_height)
                        first_contact = True

                    # remove mirror bug
                    if height_on_screen < 0:
                        height_on_screen = 0

                    # draw vert line
                    if height_on_screen < y_buffer[num_ray]:
                        for screen_y in range(height_on_screen, y_buffer[num_ray]):
                            screen_array[num_ray, screen_y] = color_map[x, y]
                        y_buffer[num_ray] = height_on_screen

        ray_angle += delta_angle
    return screen_array


class VoxelRender:
    def __init__(self, app):
        self.app = app
        self.player = app.player
        # self.fov = math.pi / 4
        self.fov = math.pi / 4
        self.h_fov = self.fov / 2
        self.num_rays = app.width
        self.delta_angle = self.fov / self.num_rays
        self.ray_distance = 2500
        self.scale_height = 920
        # self.scale_height = 220
        self.screen_array = np.full((app.width, app.height, 3), (119, 241, 255))


      


    def update(self):
        if not self.player.is_flying:
            self.player.height = height_map[int(self.player.pos[0]), int(self.player.pos[1])][0] + self.player.player_height

        self.screen_array = ray_casting(self.screen_array, self.player.pos, self.player.angle,
                                        self.player.height, self.player.pitch, self.app.width,
                                        self.app.height, self.delta_angle, self.ray_distance,
                                        self.h_fov, self.scale_height)

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)
