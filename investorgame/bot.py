
import arcade
import numpy as np
from investorgame.constants import (PATH_TO_IMAGES, SCREEN_WIDTH,
                                    SCREEN_HEIGHT, CHARACTER_SCALING)
from investorgame.utils import is_in_line_of_sight


def get_initialised_bot_sprite():
    # TODO: docstr
    bot_sprite = arcade.AnimatedWalkingSprite()

    bot_sprite.stand_right_textures = []
    bot_sprite.stand_right_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}bot/player_stand.png",
                            scale=CHARACTER_SCALING))
    bot_sprite.stand_left_textures = []
    bot_sprite.stand_left_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}bot/player_stand.png",
                            scale=CHARACTER_SCALING, mirrored=True))

    bot_sprite.walk_right_textures = []

    bot_sprite.walk_right_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}bot/player_stand.png",
                            scale=CHARACTER_SCALING))
    bot_sprite.walk_right_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}bot/player_walk1.png",
                            scale=CHARACTER_SCALING))
    bot_sprite.walk_right_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}bot/player_walk2.png",
                            scale=CHARACTER_SCALING))
    bot_sprite.walk_right_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}bot/player_walk1.png",
                            scale=CHARACTER_SCALING))

    bot_sprite.walk_left_textures = []

    bot_sprite.walk_left_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}bot/player_stand.png",
                            scale=CHARACTER_SCALING, mirrored=True))
    bot_sprite.walk_left_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}bot/player_walk1.png",
                            scale=CHARACTER_SCALING, mirrored=True))
    bot_sprite.walk_left_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}bot/player_walk2.png",
                            scale=CHARACTER_SCALING, mirrored=True))
    bot_sprite.walk_left_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}bot/player_walk1.png",
                            scale=CHARACTER_SCALING, mirrored=True))

    bot_sprite.texture_change_distance = 20
    bot_sprite.center_x = int(SCREEN_WIDTH / 2.) + 200
    bot_sprite.center_y = int(SCREEN_HEIGHT / 2.)

    return bot_sprite


def get_distance_between_sprites(sprite1, sprite2):
    # TODO: docstr
    return np.sqrt(((sprite1.center_x - sprite2.center_x)**2) +
                   ((sprite1.center_y - sprite2.center_y)**2))


def get_location_of_nearest_coin(bot_sprite, coin_list, wall_list=None):
    # TODO: docstr
    if len(coin_list) == 0:
        return None

    if wall_list is None:
        distances_from_coin = [
            get_distance_between_sprites(sprite1=bot_sprite, sprite2=coin)
            for coin in coin_list]
    else:
        distances_from_coin = [
            get_distance_between_sprites(sprite1=bot_sprite, sprite2=coin)
            for coin in coin_list
            if is_in_line_of_sight(pov_sprite=bot_sprite, object_sprite=coin,
                                   obstacle_sprite_list=wall_list)]

    nearest_coin = coin_list[np.argmin(distances_from_coin)]
    return nearest_coin.center_x, nearest_coin.center_y


def get_favoured_direction(bot_sprite, coin_list, wall_list=None):
    # TODO: docstr
    # TODO: account for walls? Add randomness?
    nearest_coin_location = get_location_of_nearest_coin(
        bot_sprite=bot_sprite, coin_list=coin_list, wall_list=wall_list)
    if nearest_coin_location is None:
        return None

    favoured_direction = (nearest_coin_location[0] - bot_sprite.center_x,
                          nearest_coin_location[1] - bot_sprite.center_y)
    return favoured_direction
