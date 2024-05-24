import pygame as pg

class HUD:
    def __init__(self,screen, height_map_img, color_map_img, player):
        self.name = "HUD"
        self.screen = screen
        self.height_map_img = height_map_img
        self.color_map_img = color_map_img
        self.player = player

        self.hud_size = (100,100)
        self.hud_pos = (0,self.screen.get_height()-self.hud_size[1])
        self.hud_offset_x = self.hud_size[0]//2
        self.hud_offset_y = self.hud_size[1]//2

    def draw(self):
        px = int(self.player.pos[0]) % self.color_map_img.get_width()
        py = int(self.player.pos[1]) % self.color_map_img.get_height()
        self.screen.blit(self.color_map_img, self.hud_pos, (px - self.hud_offset_x ,py - self.hud_offset_y, self.hud_size[0],self.hud_size[1]))
        pg.draw.circle(self.screen,(255,0,0),(self.hud_pos[0]+self.hud_offset_x ,self.hud_pos[1]+self.hud_offset_y),4,2)
