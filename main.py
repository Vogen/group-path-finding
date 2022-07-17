import random
import arcade

from solver import Solver

# --- Constants ---
CHARACTER_SPRITE_RADIUS = 10
TARGET_SPRITE_RADIUS = 5
HEAD_SPRITE_RADIUS = 5
FORMATION_PADDING = 30
FORMATION_LIST = [5, 5]
# FORMATION_LIST = [1, 2, 3, 4, 5]
CHARACTER_NUM = sum(FORMATION_LIST)
CHARACTER_SPEED = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Group Path Finding"

class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Variables that will hold sprite lists
        self.character_sprite_list = None
        self.target_sprite_list = None

        # Don't show the mouse cursor
        self.set_mouse_visible(True)

        arcade.set_background_color(arcade.color.AMAZON)
        
        self.move_dict = None
        self.head_character = None
        self.head_target = None
        self.head_sprite = None

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.character_sprite_list = arcade.SpriteList()
        self.target_sprite_list = arcade.SpriteList()
        self.move_dict = {}

        # Create the characters
        for i in range(CHARACTER_NUM):

            # Create the character instance
            character = arcade.SpriteCircle(CHARACTER_SPRITE_RADIUS, (84, 187, 255))
            character.center_x = SCREEN_WIDTH / 2  + random.uniform(-100, 100)
            character.center_y = SCREEN_HEIGHT / 2 + random.uniform(-100, 100)

            # Add the character to the lists
            self.character_sprite_list.append(character)

            target = arcade.SpriteCircle(TARGET_SPRITE_RADIUS, (173, 216, 230))
            self.target_sprite_list.append(target)
        
        # Create head mark
        self.head_sprite = arcade.SpriteCircle(HEAD_SPRITE_RADIUS, (255,140,0))

    def on_draw(self):
        """ Draw everything """
        
        self.clear()
        self.character_sprite_list.draw()
        self.target_sprite_list.draw()
        self.head_sprite.draw()

        # Put the text on the screen.
        # output = f"Score: {self.score}"
        # arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if len(FORMATION_LIST) == 0: return

        head_index = int((FORMATION_LIST[0] - 1) / 2)
        self.head_target = self.target_sprite_list[head_index]

        # calc target rotation
        cx_avg = sum([s.center_x for s in self.character_sprite_list]) / len(self.character_sprite_list)
        cy_avg = sum([s.center_y for s in self.character_sprite_list]) / len(self.character_sprite_list)
        dx = x - cx_avg
        dy = y - cy_avg
        d = pow(pow(dx, 2) + pow(dy, 2), 0.5)
        sin_theta = dy / d
        cos_theta = dx / d

        # calc target offset
        target_index = 0
        for i, n in enumerate(FORMATION_LIST):
            c = (n - 1) / 2
            for j in range(n):
                dx = (j - c) * FORMATION_PADDING
                dy = (  - i) * FORMATION_PADDING

                target = self.target_sprite_list[target_index]
                target.center_x = x + sin_theta * dx + cos_theta * dy
                target.center_y = y - cos_theta * dx + sin_theta * dy
                target_index += 1

        tx_avg = sum([s.center_x for s in self.target_sprite_list]) / len(self.target_sprite_list)
        ty_avg = sum([s.center_y for s in self.target_sprite_list]) / len(self.target_sprite_list)

        # Assign Target
        start  = [[s.center_x - cx_avg, s.center_y - cy_avg, s] for s in self.character_sprite_list]
        target = [[s.center_x - tx_avg, s.center_y - ty_avg, s] for s in self.target_sprite_list]
        solver = Solver()
        match, cost = solver.solve(start, target)
        for _, e in match.items():
            self.move_dict[e.s.v] = e.t.v
            if e.t.v == self.head_target:
                self.head_character = e.s.v


    def on_update(self, delta_time):
        """ Movement and game logic """

        self.character_sprite_list.update()
        self.target_sprite_list.draw()

        for character, target in self.move_dict.items():
            cx, cy = character.center_x, character.center_y
            tx, ty = target.center_x, target.center_y
            
            # use relative target
            if not character == self.head_character:
                tx += self.head_character.center_x - self.head_target.center_x
                ty += self.head_character.center_y - self.head_target.center_y

            dx, dy = tx - cx, ty - cy
            d = pow(pow(dx, 2) + pow(dy, 2), 0.5)
            if d > 1:
                step = delta_time * CHARACTER_SPEED
                if d < step:
                    character.center_x = tx
                    character.center_y = ty
                else:
                    fx, fy = dx / d, dy / d
                    mx, my = fx * step, fy * step
                    character.center_x += mx
                    character.center_y += my

        if self.head_character:
            self.head_sprite.center_x = self.head_character.center_x
            self.head_sprite.center_y = self.head_character.center_y
            
        # Generate a list of all sprites that collided with the player.
        # hit_list = arcade.check_for_collision_with_list(self.player_sprite,
        #                                                 self.coin_sprite_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        # for coin in hit_list:
        #     coin.remove_from_sprite_lists()
        #     self.score += 1


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()