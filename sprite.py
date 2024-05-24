import math
class Sprite:
    def __init__(self, position, texture):
        self.position = position
        self.texture = texture
        self.screen_x = 0
        self.screen_y = 0
        self.size = 0
        self.distance = 0

    def transform_sprite(self, sprite, player_pos, player_angle, player_height, screen_width, screen_height, fov, scale_height):
        dx = sprite.position[0] - player_pos[0]
        dy = sprite.position[1] - player_pos[1]
        dz = sprite.position[2] - player_height  # Assuming sprite.position has a z component for height

        distance = math.sqrt(dx**2 + dy**2 + dz**2)
        sprite.distance = distance

        angle = math.atan2(dy, dx) - player_angle
        sprite.screen_x = int(screen_width / 2 * (1 + math.tan(angle) / math.tan(fov / 2)))
        sprite.screen_y = int(screen_height / 2 * (1 - dz / distance * scale_height))
        sprite.size = int(screen_height / distance * scale_height)