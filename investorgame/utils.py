
import numpy as np


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

        round_closest_x_fn = (lambda x: int(np.floor(x)))
        round_furthest_x_fn = (lambda x: int(np.ceil(x)))
        round_closest_y_fn = (lambda y: int(np.ceil(y)))
        round_furthest_y_fn = (lambda y: int(np.floor(y)))
    elif closest_x_index == 0 and closest_y_index == 1:
        closest_x = left
        furthest_x = right
        closest_y = bottom
        furthest_y = top

        round_closest_x_fn = (lambda x: int(np.floor(x)))
        round_furthest_x_fn = (lambda x: int(np.ceil(x)))
        round_closest_y_fn = (lambda y: int(np.floor(y)))
        round_furthest_y_fn = (lambda y: int(np.ceil(y)))
    elif closest_x_index == 1 and closest_y_index == 0:
        closest_x = right
        furthest_x = left
        closest_y = top
        furthest_y = bottom

        round_closest_x_fn = (lambda x: int(np.ceil(x)))
        round_furthest_x_fn = (lambda x: int(np.floor(x)))
        round_closest_y_fn = (lambda y: int(np.ceil(y)))
        round_furthest_y_fn = (lambda y: int(np.floor(y)))
    elif closest_x_index == 1 and closest_y_index == 1:
        closest_x = right
        furthest_x = left
        closest_y = bottom
        furthest_y = top

        round_closest_x_fn = (lambda x: int(np.ceil(x)))
        round_furthest_x_fn = (lambda x: int(np.floor(x)))
        round_closest_y_fn = (lambda y: int(np.floor(y)))
        round_furthest_y_fn = (lambda y: int(np.ceil(y)))
    else:
        raise ValueError(f"unable to detect new position relative to location "
                         f"(closest_x_index {closest_x_index}, "
                         f"closest_y_index {closest_y_index})")

    def _get_grid_points(obj_x, round_x_fn, obj_y, round_y_fn):
        gradient = float((obj_x - location[0]) / (obj_y - location[1]))
        intercept = location[1] - (gradient * location[0])
        get_y_given_x = (lambda x: round_y_fn(intercept + (gradient * x)))
        get_x_given_y = (lambda y: round_x_fn((y - intercept) / gradient))
        return (
            [(x, get_y_given_x(x)) for x in range(location[0], obj_x + 1)] +
            [(get_x_given_y(y), y) for y in range(location[1], obj_y + 1)])

    grid_points = [
        _get_grid_points(obj_x=obj_x, round_x_fn=round_x_fn, obj_y=obj_y,
                         round_y_fn=round_y_fn)
        for obj_x, round_x_fn, obj_y, round_y_fn in [
            (closest_x, round_closest_x_fn, furthest_y, round_furthest_y_fn),
            (furthest_x, round_furthest_x_fn, closest_y, round_closest_y_fn)]]
    return grid_points

    # TODO:
    #  - do for furthest_x and closest_y too
    #  - return grid points, and use to work out if a list sprites blocks the sight

    print('debugging')  # TODO: remove!!


if __name__ == '__main__':
    get_line_of_sight_grid((10, 5), left=21, right=23, top=17, bottom=15)
