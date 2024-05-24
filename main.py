import pygame as pg
from player import Player
# from voxel_render import VoxelRender
from voxel_render_c import VoxelRender
from settings import GAME_SETTINGS

class App:
    def __init__(self):
        self.res = self.width, self.height = GAME_SETTINGS["resolution"]
        self.screen = pg.display.set_mode(self.res, pg.SCALED)
        self.clock = pg.time.Clock()
        self.player = Player()
        self.voxel_render = VoxelRender(self)

    def update(self):
        self.player.update()
        self.voxel_render.update()

        pg.event.set_grab(self.player.lock_mouse)
        pg.mouse.set_visible(not self.player.lock_mouse)
        mouse_rel = pg.mouse.get_rel()
        self.player.handle_mouse(mouse_rel)

    def draw(self):
        self.voxel_render.draw()
        pg.display.flip()

    def run(self):
        while True:
            self.update()
            self.draw()

            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick(100)
            pg.display.set_caption(f'VOXELIA | FPS: {int(self.clock.get_fps())}')


if __name__ == '__main__':
    app = App()
    app.run()
