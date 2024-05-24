import math
import pygame as pg
GAME_SETTINGS = {
    "resolution":(640,360),
    "fov": math.pi / 3,
    "render_distance": 1500,
    "height_scale": 200,
    "sky_color": (119, 241, 255),
    "height_map": "img/D10_1.png",
    "color_map": "img/C10.png"
}
GAME_CONTROLS = {
    "look_up": pg.K_UP,
    "look_down": pg.K_DOWN,
    "look_left": pg.K_LEFT,
    "look_right": pg.K_RIGHT,
    "go_up": pg.K_q,
    "go_down": pg.K_e,
    "forward": pg.K_w,
    "backward": pg.K_s,
    "strafe_left": pg.K_a,
    "strafe_right": pg.K_d,
    "fly_toggle": pg.K_SPACE,
    "mouse_toggle": pg.K_TAB,
    "quit": pg.K_ESCAPE
}

MOUSE_CONTROLS = {
    "mouse_x_sensitivity": 0.0005,
    "mouse_y_sensitivity": 0.5
}