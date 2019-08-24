
import arcade
import random
import numpy as np
from copy import deepcopy
from game_constants import (PATH_TO_IMAGES, SCREEN_WIDTH, SCREEN_HEIGHT,
    SCREEN_TITLE, CHARACTER_SCALING, TILE_SCALING, COIN_SCALING,
    PLAYER_MOVEMENT_SPEED, LEFT_VIEWPORT_MARGIN, RIGHT_VIEWPORT_MARGIN,
    BOTTOM_VIEWPORT_MARGIN, TOP_VIEWPORT_MARGIN)
from player import get_initialised_player_sprite
from bot import get_initialised_bot_sprite, get_favoured_direction

# TODO: WHY DOES THE BOT JUMP AROUND??
# TODO: WHY HAS THE COMPUTER STOPPED WORKING? IS IT DUE TO THE MULTIPLE PHYSICS ENGINES?

# TODO: add inflation
# TODO: add retirement etc
# TODO: add variation in income opportunity - could pay money to get
#  up-skilled, resulting in the coins being worth more; over time skills
#  already gained should depreciate (and this should be shown in text so that
#  the player knows what's going on, could even have announcements on when new
#  technology is released)
# TODO: add out-goings - rent unless a place is bought (then mortgage)

# TODO: for returns, could randomly sample (with replacement) from actual
#  returns from a global etf between years (e.g.) 1990 and 2018


class InvestorGame(arcade.Window):
    """Investor game"""
    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.wall_list = None
        self.player_list = None
        self.bot_list = None
        self.computer_sprite = None
        self.item_list = None
        self.coin_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None
        self.player_info = None

        self.bot_sprite = None
        self.bot_helper_sprite = None

        # Our physics engine
        self.player_physics_engine = None
        self.bot_physics_engine = None
        self.bot_helper_physics_engine = None
        self.total_game_seconds = None

        # Used to keep track of our scrolling
        self.view_bottom = None
        self.view_left = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.current_state = 'top_down_view_running'
        self.computer_state = 'login'
        self.computer = arcade.load_texture(
            f"{PATH_TO_IMAGES}backgrounds/computer_screen.png")

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        self._create_wall_list()
        self._create_player_list()
        self._create_bot_list()
        self._create_bot_helper_list()
        self._setup_player()
        self._setup_bot()
        self._setup_bot_helper()
        self._create_item_list()
        self._setup_computer()
        self._create_coin_list()

        # Create the 'physics engine'
        player_walls = deepcopy(self.wall_list)
        player_walls.append(self.bot_sprite)
        self.player_physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, player_walls)
        self.total_game_seconds = 0.

        bot_walls = deepcopy(self.wall_list)
        bot_walls.append(self.player_sprite)
        for item in self.item_list:
            bot_walls.append(item)

        bot_helper_walls = deepcopy(bot_walls)
        self.bot_physics_engine = arcade.PhysicsEngineSimple(
            self.bot_sprite, bot_walls)
        self.bot_helper_physics_engine = arcade.PhysicsEngineSimple(
            self.bot_helper_sprite, bot_helper_walls)
        # TODO: is this separate physics engine necessary?

        self.player_info = {
            'age': 22,
            'current_money': 0.,
            'isa_money': 0.,
        }

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen to the background color
        arcade.start_render()

        if self.current_state == 'top_down_view_running':
            self._draw_running_top_down_view()
        elif self.current_state == 'computer_running':
            self._draw_running_computer()
        elif self.current_state == 'game_end':
            self._draw_game_end()
        else:
            raise ValueError(f"unrecognised current_state "
                             f"{self.current_state}")

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if self.current_state == 'top_down_view_running':
            self._on_key_press_running_top_down_view(key, modifiers)
        elif self.current_state == 'computer_running':
            self._on_key_press_running_computer(key, modifiers)
        else:
            raise ValueError(f"unrecognised current_state "
                             f"{self.current_state}")

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """
        year_start = self._get_current_year()
        day_start = self._get_day_in_current_year()

        if self.current_state == 'top_down_view_running':
            self._update_top_down_view_running()
            self.total_game_seconds += delta_time

        year_end = self._get_current_year()
        if year_start < year_end:
            self.player_info['age'] += 1
            self._update_player_current_money()
            self._create_coin_list()

        day_end = self._get_day_in_current_year()
        n_days_past = day_end - day_start
        if n_days_past > 0:
            for _ in range(n_days_past):
                self._update_player_isa_money()

        if self.player_info['age'] == 60:
            self.current_state = 'game_end'

    def _create_player_list(self):
        self.player_list = arcade.SpriteList()

    def _setup_player(self):
        self.player_sprite = get_initialised_player_sprite()
        self.player_list.append(self.player_sprite)

    def _create_bot_list(self):
        self.bot_list = arcade.SpriteList()

    def _create_bot_helper_list(self):
        self.bot_helper_list = arcade.SpriteList()

    def _setup_bot(self):
        self.bot_sprite = get_initialised_bot_sprite()
        self.bot_list.append(self.bot_sprite)

    def _setup_bot_helper(self):
        self.bot_helper_sprite = get_initialised_bot_sprite()
        self.bot_helper_list.append(self.bot_helper_sprite)

    def _create_wall_list(self):
        # place horizontally (using multiple sprites)
        self.wall_list = arcade.SpriteList()
        for x in range(0, 500):
            for y in [20, 500]:
                wall = arcade.Sprite(f"{PATH_TO_IMAGES}tiles/foliagePack_leaves_002.png", TILE_SCALING)
                wall.center_x = x
                wall.center_y = y
                self.wall_list.append(wall)

        # place vertically (using multiple sprites)
        for y in range(20, 500):
            wall = arcade.Sprite(f"{PATH_TO_IMAGES}tiles/foliagePack_leaves_002.png", TILE_SCALING)
            wall.center_x = 0
            wall.center_y = y
            self.wall_list.append(wall)

    def _create_item_list(self):
        self.item_list = arcade.SpriteList()

    def _setup_computer(self):
        self.computer_sprite = arcade.Sprite(
            f"{PATH_TO_IMAGES}items/genericItem_color_050.png", scale=0.75)
        self.computer_sprite.center_x = 100
        self.computer_sprite.center_y = 400
        self.item_list.append(self.computer_sprite)

    def _create_coin_list(self):
        self.coin_list = arcade.SpriteList()
        for i in range(50):
            # Create the coin instance
            coin = arcade.Sprite(f"{PATH_TO_IMAGES}items/bronze_1.png", COIN_SCALING)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            coin_placed_well = True
            for sprite_list in [self.player_list, self.wall_list,
                                self.item_list, self.bot_list]:
                for s in sprite_list:
                    if arcade.check_for_collision(coin, s):
                        coin_placed_well = False
                        break

            if coin_placed_well:
                self.coin_list.append(coin)

    def _draw_running_top_down_view(self):
        self.wall_list.draw()
        self.player_list.draw()
        self.bot_list.draw()
        self.item_list.draw()
        self.coin_list.draw()

        self._draw_background_text()

    def _draw_running_computer(self):
        self._draw_background_text()

        page_texture = self.computer
        arcade.draw_texture_rectangle(self.view_left + (SCREEN_WIDTH / 2.),
                                      self.view_bottom + (SCREEN_HEIGHT / 2.),
                                      page_texture.width, page_texture.height,
                                      page_texture, 0)

        if self.computer_state == 'login':
            text = ("Log into the website\nof your stocks and\nshares ISA "
                    "provider?\n(y/n)\n")
        elif self.computer_state == 'deposit_question':
            isa_money = self.player_info['isa_money']
            text = (f"Account balance: £{np.round(isa_money, 2)}\n"
                    f"\nDeposit money?\n(y/n)\n")
        elif self.computer_state == 'deposit_amount':
            text = ("How much would you\nlike to deposit?\n\n0 - back\n1 - "
                    "100\n2 - 200\n3 - 500\n4 - 1000\n")
        elif self.computer_state == 'fund_problem':
            text = "Not enough funds.\n\nReturn to deposit screen?\n(y/n)\n"
        else:
            raise ValueError(f"unrecognised computer_state "
                             f"{self.computer_state}")

        arcade.draw_text(
            text, self.view_left + (SCREEN_WIDTH / 3.),
            self.view_bottom + (SCREEN_HEIGHT / 2.),
            arcade.color.BLACK, 20, bold=True)

    def _draw_game_end(self):
        self._draw_background_text()
        arcade.draw_text(
            'End of game\n', self.view_left + (SCREEN_WIDTH / 3.),
            self.view_bottom + (SCREEN_HEIGHT / 2.),
            arcade.color.BLACK, 20, bold=True)

    def _on_key_press_running_top_down_view(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def _on_key_press_running_computer(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.current_state = 'top_down_view_running'
            self.player_sprite.center_x = int(SCREEN_WIDTH / 2.)
            self.player_sprite.center_y = int(SCREEN_HEIGHT / 2.)

        if self.computer_state == 'login':
            if key == arcade.key.Y:
                self.computer_state = 'deposit_question'
            elif key == arcade.key.N:
                self.current_state = 'top_down_view_running'
                self.player_sprite.center_x = int(SCREEN_WIDTH / 2.)
                self.player_sprite.center_y = int(SCREEN_HEIGHT / 2.)

        elif self.computer_state == 'deposit_question':
            if key == arcade.key.Y:
                self.computer_state = 'deposit_amount'
            elif key == arcade.key.N:
                self.computer_state = 'login'

        elif self.computer_state == 'deposit_amount':
            if key in [arcade.key.NUM_0, arcade.key.KEY_0]:
                self.computer_state = 'deposit_question'
            elif key in [arcade.key.NUM_1, arcade.key.NUM_2, arcade.key.NUM_3,
                         arcade.key.NUM_4, arcade.key.KEY_1, arcade.key.KEY_2,
                         arcade.key.KEY_3, arcade.key.KEY_4]:
                if key in [arcade.key.NUM_1, arcade.key.KEY_1]:
                    money = 100
                elif key in [arcade.key.NUM_2, arcade.key.KEY_2]:
                    money = 200
                elif key in [arcade.key.NUM_3, arcade.key.KEY_3]:
                    money = 500
                elif key in [arcade.key.NUM_4, arcade.key.KEY_4]:
                    money = 1000
                else:
                    raise ValueError(f"unrecognised key {key}")

                if self.player_info['current_money'] < money:
                    self.computer_state = 'fund_problem'
                else:
                    self.player_info['current_money'] -= money
                    self.player_info['isa_money'] += money
                    self.computer_state = 'deposit_question'

        elif self.computer_state == 'fund_problem':
            if key == arcade.key.Y:
                self.computer_state = 'deposit_amount'
            elif key == arcade.key.N:
                self.computer_state = 'login'

        else:
            raise ValueError(f"unrecognised computer_state "
                             f"{self.computer_state}")

    def _draw_background_text(self):
        year = self._get_current_year()
        current_money = np.round(self.player_info['current_money'], 2)
        isa_money = np.round(self.player_info['isa_money'], 2)
        arcade.draw_text(
            f"Year: {year}\n"
            f"Age: {self.player_info['age']}\n"
            f"Current account: £{current_money}\n"
            f"Stocks and shares ISA: £{isa_money}\n",
            self.view_left + (LEFT_VIEWPORT_MARGIN / 2.),
            self.view_bottom + SCREEN_HEIGHT - (TOP_VIEWPORT_MARGIN * 1.1),
            arcade.color.BLACK, 20, bold=True)

    def _get_current_year(self):
        return int(self.total_game_seconds) // 20

    def _get_prop_through_current_year(self):
        return (int(self.total_game_seconds) % 20) / 20.

    def _get_day_in_current_year(self):
        return int(self._get_prop_through_current_year() * 365)

    def _update_player_current_money(self):
        self.player_info['current_money'] += (
            self.player_info['current_money'] * 0.01)
        # TODO: interest paid should depend on the proportion of the year that
        #  money is in the account

    def _update_player_isa_money(self):
        loc_ = 0.0002  # note: annualised_return = ((1 + loc_) ** 365) - 1
        scale_ = 0.005
        returns = np.maximum(
            -0.1, np.minimum(0.1, np.random.normal(loc=loc_, scale=scale_)))
        self.player_info['isa_money'] += (
            self.player_info['isa_money'] * returns)

    def _update_top_down_view_running(self):
        # Call update on all sprites
        self.player_physics_engine.update()
        self._handle_coin_collection()
        self._handle_computer_collision()
        self._update_bot()
        self.bot_physics_engine.update()
        for c in self.coin_list:
            if arcade.check_for_collision(self.bot_sprite, c):
                c.kill()

        self.player_list.update_animation()
        self.bot_list.update_animation()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def _handle_coin_collection(self):
        for c in self.coin_list:
            if arcade.check_for_collision(self.player_sprite, c):
                c.kill()
                self.player_info['current_money'] += 10

    def _handle_computer_collision(self):
        if arcade.check_for_collision(self.player_sprite,
                                      self.computer_sprite):
            self.computer_state = 'login'
            self.current_state = 'computer_running'

    def _update_bot(self):
        favoured_direction = get_favoured_direction(
            bot_sprite=self.bot_sprite, coin_list=self.coin_list)
        if favoured_direction is None:
            self.bot_sprite.change_x = 0
            self.bot_sprite.change_y = 0
            return None

        if not self._is_direction_good(direction=favoured_direction):
            self.bot_sprite.change_x = 0
            self.bot_sprite.change_y = 0
            return None

        def _get_change_x_y(speed_, direction_):
            dir_x = int(direction_[0])
            dir_y = int(direction_[1])
            change_x = int(np.sign(dir_x) * min(speed_, np.abs(dir_x)))
            change_y = int(np.sign(dir_y) * min(speed_, np.abs(dir_y)))
            return change_x, change_y

        bot_speed = int(PLAYER_MOVEMENT_SPEED / 3.)
        change_x_y = _get_change_x_y(speed_=bot_speed,
                                     direction_=favoured_direction)
        self.bot_sprite.change_x = change_x_y[0]
        self.bot_sprite.change_y = change_x_y[1]

        # self.bot_physics_engine.update()

        # for c in self.coin_list:
        #     if arcade.check_for_collision(self.bot_sprite, c):
        #         c.kill()

    def _is_direction_good(self, direction):
        self.bot_helper_sprite.center_x = int(self.bot_sprite.center_x)
        self.bot_helper_sprite.center_y = int(self.bot_sprite.center_y)
        self.bot_helper_sprite.change_x = int(direction[0])
        self.bot_helper_sprite.change_y = int(direction[1])
        self.bot_helper_physics_engine.update()
        self.bot_helper_list.update_animation()
        return any([arcade.check_for_collision(self.bot_helper_sprite, c)
                    for c in self.coin_list])


def main():
    """ Main method """
    window = InvestorGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
