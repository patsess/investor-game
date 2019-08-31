
import arcade
import numpy as np
from shapely.geometry import Polygon


def is_in_line_of_sight(pov_sprite, object_sprite, obstacle_sprite_list):
    # TODO: doctr
    p1_location = (pov_sprite.center_x, pov_sprite.center_y)
    p1_points = get_line_of_sight_helper_grid_points(
        location=p1_location,
        left=object_sprite.left, right=object_sprite.right,
        top=object_sprite.top, bottom=object_sprite.bottom)
    p1 = Polygon([p1_location] + p1_points)

    line_of_sight = (
        not any([p1.intersects(Polygon(
            [(s.left, s.top), (s.right, s.top), (s.right, s.bottom),
             (s.left, s.bottom)])) for s in obstacle_sprite_list]))
    return line_of_sight
    # TODO: change it to using the centre of the object sprite?


def get_line_of_sight_helper_grid_points(location, left, right, top, bottom):
    # TODO: docstr
    # TODO: probably replace arguments with a sprite
    closest_x_index = np.argmin(
        [np.abs(location[0] - left), np.abs(location[0] - right)])
    closest_y_index = np.argmin(
        [np.abs(location[1] - top), np.abs(location[1] - bottom)])

    if closest_x_index == 0 and closest_y_index == 0:
        closest_x = left
        furthest_x = right
        closest_y = top
        furthest_y = bottom

        # round_closest_x_fn = (lambda x: int(np.floor(x)))
        # round_furthest_x_fn = (lambda x: int(np.ceil(x)))
        # round_closest_y_fn = (lambda y: int(np.ceil(y)))
        # round_furthest_y_fn = (lambda y: int(np.floor(y)))

    elif closest_x_index == 0 and closest_y_index == 1:
        closest_x = left
        furthest_x = right
        closest_y = bottom
        furthest_y = top

        # round_closest_x_fn = (lambda x: int(np.floor(x)))
        # round_furthest_x_fn = (lambda x: int(np.ceil(x)))
        # round_closest_y_fn = (lambda y: int(np.floor(y)))
        # round_furthest_y_fn = (lambda y: int(np.ceil(y)))

    elif closest_x_index == 1 and closest_y_index == 0:
        closest_x = right
        furthest_x = left
        closest_y = top
        furthest_y = bottom

        # round_closest_x_fn = (lambda x: int(np.ceil(x)))
        # round_furthest_x_fn = (lambda x: int(np.floor(x)))
        # round_closest_y_fn = (lambda y: int(np.ceil(y)))
        # round_furthest_y_fn = (lambda y: int(np.floor(y)))

    elif closest_x_index == 1 and closest_y_index == 1:
        closest_x = right
        furthest_x = left
        closest_y = bottom
        furthest_y = top

        # round_closest_x_fn = (lambda x: int(np.ceil(x)))
        # round_furthest_x_fn = (lambda x: int(np.floor(x)))
        # round_closest_y_fn = (lambda y: int(np.floor(y)))
        # round_furthest_y_fn = (lambda y: int(np.ceil(y)))

    else:
        raise ValueError(f"unable to detect new position relative to location "
                         f"(closest_x_index {closest_x_index}, "
                         f"closest_y_index {closest_y_index})")

    # def _get_grid_points(obj_x, round_x_fn, obj_y, round_y_fn):
    #     gradient = float((obj_x - location[0]) / (obj_y - location[1]))
    #     intercept = location[1] - (gradient * location[0])
    #     get_y_given_x = (lambda x: round_y_fn(intercept + (gradient * x)))
    #     get_x_given_y = (lambda y: round_x_fn((y - intercept) / gradient))
    #     return (
    #         [(x, get_y_given_x(x)) for x in range(location[0], obj_x + 1)] +
    #         [(get_x_given_y(y), y) for y in range(location[1], obj_y + 1)])
    #
    # grid_points = [
    #     _get_grid_points(obj_x=obj_x, round_x_fn=round_x_fn, obj_y=obj_y,
    #                      round_y_fn=round_y_fn)
    #     for obj_x, round_x_fn, obj_y, round_y_fn in [
    #         (closest_x, round_closest_x_fn, furthest_y, round_furthest_y_fn),
    #         (furthest_x, round_furthest_x_fn, closest_y, round_closest_y_fn)]]

    grid_points = [(int(closest_x), int(furthest_y)),
                   (int(furthest_x), int(closest_y))]
    return grid_points


def is_line_of_sight_clear(grid_points, object_sprite_list):
    # TODO: docstr
    for obj_sprite in object_sprite_list:
        if arcade.geometry.are_polygons_intersecting(grid_points,
                                                     obj_sprite.points):
            return False

    return True


if __name__ == '__main__':
    grid_points = get_line_of_sight_helper_grid_points(
        (10, 5), left=21, right=23, top=17, bottom=15)
