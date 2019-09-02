
import arcade
from investorgame.constants import (PATH_TO_IMAGES, SCREEN_WIDTH,
    SCREEN_HEIGHT, CHARACTER_SCALING)


def get_initialised_player_sprite():
    player_sprite = arcade.AnimatedWalkingSprite()

    player_sprite.stand_right_textures = []
    player_sprite.stand_right_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}player_1/female_stand.png",
                            scale=CHARACTER_SCALING))
    player_sprite.stand_left_textures = []
    player_sprite.stand_left_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}player_1/female_stand.png",
                            scale=CHARACTER_SCALING, mirrored=True))

    player_sprite.walk_right_textures = []

    player_sprite.walk_right_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}player_1/female_stand.png",
                            scale=CHARACTER_SCALING))
    player_sprite.walk_right_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}player_1/female_walk1.png",
                            scale=CHARACTER_SCALING))
    player_sprite.walk_right_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}player_1/female_walk2.png",
                            scale=CHARACTER_SCALING))
    player_sprite.walk_right_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}player_1/female_walk1.png",
                            scale=CHARACTER_SCALING))

    player_sprite.walk_left_textures = []

    player_sprite.walk_left_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}player_1/female_stand.png",
                            scale=CHARACTER_SCALING, mirrored=True))
    player_sprite.walk_left_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}player_1/female_walk1.png",
                            scale=CHARACTER_SCALING, mirrored=True))
    player_sprite.walk_left_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}player_1/female_walk2.png",
                            scale=CHARACTER_SCALING, mirrored=True))
    player_sprite.walk_left_textures.append(
        arcade.load_texture(f"{PATH_TO_IMAGES}player_1/female_walk1.png",
                            scale=CHARACTER_SCALING, mirrored=True))

    player_sprite.texture_change_distance = 20
    player_sprite.center_x = int(SCREEN_WIDTH / 2.)
    player_sprite.center_y = int(SCREEN_HEIGHT / 2.)

    return player_sprite
