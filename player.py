import pygame as pg
import numpy as np
import math
from settings import GAME_CONTROLS, MOUSE_CONTROLS, GAME_SETTINGS

class Player:
    def __init__(self):
        self.pos = np.array([0, 0], dtype=float)
        self.angle = math.pi / 4
        self.height = 270
        self.pitch = 40
        self.angle_vel = 0.02
        self.vel = 3
        self.is_flying = False
        self.player_height = GAME_SETTINGS["player_height"]
        self.mouse_y_sensitivity = MOUSE_CONTROLS["mouse_y_sensitivity"]
        self.mouse_x_sensitivity = MOUSE_CONTROLS["mouse_x_sensitivity"]
        self.lock_mouse = False

        self.pitch_tresh = 220
        self.pitch_up_offset = 150


    def handle_mouse(self, mouse_rel):
        self.angle += mouse_rel[0] * self.mouse_x_sensitivity
        self.pitch -= mouse_rel[1] * self.mouse_y_sensitivity

        if self.pitch < -self.pitch_tresh:
            self.pitch = -self.pitch_tresh

        if self.pitch > self.pitch_tresh + self.pitch_up_offset:
            self.pitch = self.pitch_tresh + self.pitch_up_offset

    def update(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        pressed_key = pg.key.get_pressed()
        
        if pressed_key[GAME_CONTROLS["look_up"]]:
            self.pitch += self.vel * 3
        if pressed_key[GAME_CONTROLS["look_down"]]:
            self.pitch -= self.vel * 3

        if pressed_key[GAME_CONTROLS["look_left"]]:
            self.angle -= self.angle_vel
        if pressed_key[GAME_CONTROLS["look_right"]]:
            self.angle += self.angle_vel

        if pressed_key[GAME_CONTROLS["go_up"]]:
            self.height += self.vel
        if pressed_key[GAME_CONTROLS["go_down"]]:
            self.height -= self.vel

        if pressed_key[GAME_CONTROLS["forward"]]:
            self.pos[0] += self.vel * cos_a
            self.pos[1] += self.vel * sin_a
        if pressed_key[GAME_CONTROLS["backward"]]:
            self.pos[0] -= self.vel * cos_a
            self.pos[1] -= self.vel * sin_a
        if pressed_key[GAME_CONTROLS["strafe_left"]]:
            self.pos[0] += self.vel/2 * sin_a
            self.pos[1] -= self.vel/2 * cos_a
        if pressed_key[GAME_CONTROLS["strafe_right"]]:
            self.pos[0] -= self.vel/2 * sin_a
            self.pos[1] += self.vel/2 * cos_a

        if pressed_key[GAME_CONTROLS["fly_toggle"]]:
            self.is_flying = not self.is_flying

        if pressed_key[GAME_CONTROLS["mouse_toggle"]]:
            print("Lock/unlock mouse")
            self.lock_mouse = not self.lock_mouse

        if pressed_key[GAME_CONTROLS["quit"]]:
            print("bye!")
            exit()


