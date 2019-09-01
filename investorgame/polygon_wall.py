
import arcade
import numpy as np

__author__ = 'psessford'

# TODO
# make each (peice of straight) wall a single polygone.
# - maybe could even loop through wall sprite and work out optimal polygones.
# - maybe for a specified polygone, work out the optomial wall sprites to fill/create it.
#
# show bot's bank balance, who doesn't have an isa. Could add another player.


class PolygonWall(object):
    # TODO: docstr
    def __init__(self, wall_left, wall_right, wall_top, wall_bottom,
                 sprite_image):
        # TODO: docstr
        assert (wall_left < wall_right)
        assert (wall_bottom < wall_top)
        self.wall_left = wall_left
        self.wall_right = wall_right
        self.wall_top = wall_top
        self.wall_bottom = wall_bottom

        self.sprite_image = sprite_image

        # helpers for properties
        self._wall_polygon_points = None
        self._wall_size = None
        self._unscaled_sprite_size = None
        self._is_wall_horizontal = None
        self._example_unscaled_sprite = None

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
    def wall_size(self):
        if self._wall_size is None:
            self._wall_size = (self.wall_right - self.wall_left,
                               self.wall_top - self.wall_bottom)

        return self._wall_size

    @property
    def unscaled_sprite_size(self):
        if self._unscaled_sprite_size is None:
            unscaled_sprite = self.example_unscaled_sprite
            assert (unscaled_sprite.left < unscaled_sprite.right)
            assert (unscaled_sprite.bottom < unscaled_sprite.top)
            self._unscaled_sprite_size = (
                unscaled_sprite.right - unscaled_sprite.left,
                unscaled_sprite.top - unscaled_sprite.bottom)

        return self._unscaled_sprite_size

    @property
    def is_wall_horizontal(self):
        if self._is_wall_horizontal is None:
            self._is_wall_horizontal = (self.wall_size[1] < self.wall_size[0])

        return self._is_wall_horizontal

    @property
    def example_unscaled_sprite(self):
        if self._example_unscaled_sprite is None:
            self._example_unscaled_sprite = arcade.Sprite(self.sprite_image,
                                                          scale=1.)

        return self._example_unscaled_sprite

    def get_sprites_to_form_wall(self):
        # TODO: docstr
        if self.is_wall_horizontal:
            sprite_scaling = (  # scale wall sprites to fill polygon vertically
                self.wall_size[1] / float(self.unscaled_sprite_size[1]))
            sprite_width = self.unscaled_sprite_size[0] * sprite_scaling
            half_sprite_width = sprite_width / 2.
            n_sprites = int(np.ceil(
                self.wall_size[0] / float(sprite_width)))
            assert (n_sprites > 0)
            end_sprite_centres_x = [self.wall_left + half_sprite_width,
                                    self.wall_right - half_sprite_width]
            sprite_gap_size = (
                (end_sprite_centres_x[1] - end_sprite_centres_x[0]) /
                float(n_sprites))
            sprite_centres_x = [
                end_sprite_centres_x[0] + (i * sprite_gap_size)
                for i in range(n_sprites)]
            sprite_centre_y = (self.wall_bottom + self.wall_top) / 2.
            wall_sprite_list = [
                arcade.Sprite(self.sprite_image, scale=sprite_scaling,
                              center_x=x, center_y=sprite_centre_y)
                for x in sprite_centres_x]
        else:
            sprite_scaling = (  # scale sprites to fill polygon horizontally
                self.wall_size[0] / float(self.unscaled_sprite_size[0]))
            sprite_height = self.unscaled_sprite_size[1] * sprite_scaling
            half_sprite_height = sprite_height / 2.
            n_sprites = int(np.ceil(
                self.wall_size[1] / float(sprite_height)))
            assert (n_sprites > 0)
            end_sprite_centres_y = [self.wall_bottom + half_sprite_height,
                                    self.wall_top - half_sprite_height]
            sprite_gap_size = (
                (end_sprite_centres_y[1] - end_sprite_centres_y[0]) /
                float(n_sprites))
            sprite_centres_y = [
                end_sprite_centres_y[0] + (i * sprite_gap_size)
                for i in range(n_sprites)]
            sprite_centre_x = (self.wall_left + self.wall_right) / 2.
            wall_sprite_list = [
                arcade.Sprite(self.sprite_image, scale=sprite_scaling,
                              center_x=sprite_centre_x, center_y=y)
                for y in sprite_centres_y]

        return wall_sprite_list


if __name__ == '__main__':
    from investorgame.game_constants import PATH_TO_IMAGES

    wall_left = 5
    wall_right = 100
    wall_top = 20
    wall_bottom = 10

    sprite_image = f"{PATH_TO_IMAGES}tiles/foliagePack_leaves_002.png"

    wall = PolygonWall(wall_left=wall_left, wall_right=wall_right,
                       wall_top=wall_top, wall_bottom=wall_bottom,
                       sprite_image=sprite_image)
    wall.get_sprites_to_form_wall()
