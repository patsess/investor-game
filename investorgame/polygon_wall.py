
import arcade

__author__ = 'psessford'


class PolygonWall(object):
    # TODO: docstr
    def __init__(self, wall_left, wall_right, wall_top, wall_bottom,
                 sprite_image):
        # TODO: docstr
        self.wall_left = wall_left
        self.wall_right = wall_right
        self.wall_top = wall_top
        self.wall_bottom = wall_bottom

        self.sprite_image = sprite_image

        # helpers for properties
        self._wall_polygon_points = None
        self._example_sprite_size = None
        self._is_wall_horizontal = None
        self._example_wall_sprite = None

    @property
    def wall_polygon_points(self):
        if self._wall_polygon_points is None:
            self._wall_polygon_points = [
                (self.wall_left, self.wall_bottom),
                (self.wall_left, self.wall_top),
                (self.wall_right, self.wall_top),
                (self.wall_right, self.wall_bottom)]

        return self._wall_polygon_points

    @property
    def example_sprite_size(self):
        if self._example_sprite_size is None:
            example_sprite = self.example_wall_sprite
            assert (example_sprite.left < example_sprite.right)
            assert (example_sprite.bottom < example_sprite.top)
            self._example_sprite_size = (
                example_sprite.right - example_sprite.left,
                example_sprite.top - example_sprite.bottom)

        return self._example_sprite_size

    @property
    def is_wall_horizontal(self):
        if self._is_wall_horizontal is None:
            self._is_wall_horizontal = (
                self.example_sprite_size[1] < self.example_sprite_size[0])

        return self._is_wall_horizontal

    @property
    def example_wall_sprite(self):
        if self._example_wall_sprite is None:
            self._example_wall_sprite = arcade.Sprite(self.sprite_image,
                                                      scale=1.)

        return self._example_wall_sprite

    def get_sprites_to_form_wall(self):
        # TODO: docstr
        example_sprite_size = self._get_example_sprite_size()
        if self.is_wall_horizontal:
            pass  # scale wall sprites to fill polygon vertically
        else:
            pass  # scale wall sprites to fill polygon horizontally

        return wall_list

    def _get_example_sprite_size(self):
        return example_sprite_size


if __name__ == '__main__':
    from investorgame.game_constants import PATH_TO_IMAGES

    wall_left = 5
    wall_right = 100
    wall_top = 20
    wall_bottom = 20

    sprite_image = f"{PATH_TO_IMAGES}tiles/foliagePack_leaves_002.png"

    wall = PolygonWall(wall_left=wall_left, wall_right=wall_right,
                       wall_top=wall_top, wall_bottom=wall_bottom,
                       sprite_image=sprite_image)
    wall.get_sprites_to_form_wall()
