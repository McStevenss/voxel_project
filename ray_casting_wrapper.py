
import ctypes
import numpy as np

# Load the shared library
# lib = ctypes.CDLL('./raycasting.so')  # Use './raycasting.dll' on Windows
lib = ctypes.CDLL('c_compiled/raycasting.so')  # Use './raycasting.dll' on Windows

# Define the argument and return types of the C function
lib.ray_casting.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),  # screen_array
    ctypes.POINTER(ctypes.c_float),  # player_pos
    ctypes.c_double,                 # player_angle
    ctypes.c_double,                 # player_height
    ctypes.c_double,                 # player_pitch
    ctypes.c_int,                    # screen_width
    ctypes.c_int,                    # screen_height
    ctypes.c_double,                 # delta_angle
    ctypes.c_int,                    # ray_distance
    ctypes.c_double,                 # h_fov
    ctypes.c_double,                 # scale_height
    ctypes.POINTER(ctypes.c_uint8),  # height_map
    ctypes.POINTER(ctypes.c_uint8),  # color_map
    ctypes.c_int,                    # map_width
    ctypes.c_int                     # map_height
]

def call_ray_casting(screen_array, player_pos, player_angle, player_height, player_pitch,
                     screen_width, screen_height, delta_angle, ray_distance, h_fov, scale_height,
                     height_map, color_map, map_width, map_height):
    
    # Convert numpy arrays to ctypes pointers
    screen_array_ctypes = screen_array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
    player_pos_ctypes = (ctypes.c_float * 2)(*player_pos)
    height_map_channel = height_map[:, :, 0]
    height_map_ctypes = height_map_channel.flatten().ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
    color_map_ctypes = color_map.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
    
    # Call the C function
    lib.ray_casting(screen_array_ctypes, player_pos_ctypes, player_angle, player_height, player_pitch,
                    screen_width, screen_height, delta_angle, ray_distance, h_fov, scale_height,
                    height_map_ctypes, color_map_ctypes, map_width, map_height)


