from random import randint
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.metrics import dp
import colorsys


class MainWidget(Widget):
    snake_parts = []
    difficulty = 20
    movex = 0
    movey = 0
    game_speed = 0.2
    game_over = False
    score = 0
    hue = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_game()
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

    def on_size(self, *args):
        self.sizex = int(self.width / self.difficulty)
        self.sizey = int(self.height / self.difficulty)
        self.update_init_game()

    def init_game(self):
        self.snake_parts = []
        self.snake_parts_positions = []
        self.movex = 0
        self.movey = 0
        self.game_over = False
        self.score = 0

        with self.canvas:
            Color(1, 1, 1)
            self.snake_parts.append(Rectangle(pos=(0, 0)))
            Color(1, 1, 1)
            self.food = Rectangle()

        # Label
        self.score_label = Label(
            text=str(self.score),
            size=(100, 100),
            font_name="lib/font.ttf",
            font_size=dp(50),
        )
        self.add_widget(self.score_label)
        Clock.schedule_interval(self.start_game, self.game_speed)

    def update_init_game(self):
        for i in self.snake_parts:
            i.size = (self.sizex, self.sizey)

        self.food.size = (self.sizex, self.sizey)
        self.food.pos = (
            self.sizex * randint(0, self.difficulty - 1),
            self.sizey * randint(0, self.difficulty - 1),
        )

        self.movex = 0
        self.movey = 0

        (x, y) = self.score_label.size
        self.score_label.pos = (int(self.width / 2 - x / 2), int(self.height / 1.15))

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard = None

    def start_game(self, *args):
        def check_free_block():
            new_pos = (
                self.sizex * randint(0, self.difficulty - 1),
                self.sizey * randint(0, self.difficulty - 1),
            )

            if not new_pos in self.snake_parts_positions:
                self.food.pos = new_pos
            else:
                check_free_block()

        # Variables
        parts_dict = dict()

        # Move body
        for i, part in enumerate(self.snake_parts):
            if i == 0:
                continue
            parts_dict[i] = self.snake_parts[i - 1].pos

        for i in range(1, len(self.snake_parts)):
            self.snake_parts[i].pos = parts_dict[i]

        # Move head
        self.head = self.snake_parts[0]
        (x, y) = self.head.pos
        self.head.pos = (x + self.movex, y + self.movey)

        # Create an array of snake positions
        self.snake_parts_positions = []

        for i in self.snake_parts:
            self.snake_parts_positions.append(i.pos)

        # Check if food collides with snake
        if self.food.pos == self.head.pos:
            with self.canvas:
                (f, g, h) = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
                Color(f, g, h)
                self.snake_parts.append(
                    Rectangle(
                        pos=self.snake_parts[-1].pos,
                        size=(self.sizex, self.sizey),
                    )
                )
                check_free_block()
                self.score += 1
                self.hue += 1 / (self.difficulty * self.difficulty)

        # Check if head collides with snake
        if self.head.pos in self.snake_parts_positions[1:]:
            self.game_over = True
        else:
            pass

        # Check if head collides with border
        (x, y) = self.head.pos
        if x == self.width:
            self.game_over = True
        elif y == self.height:
            self.game_over = True
        elif x == -self.sizex:
            self.game_over = True
        elif y == -self.sizey:
            self.game_over = True

        # Check if player won
        if self.score >= self.difficulty * self.difficulty - 1:
            self.game_over = True

        # Add counter
        self.score_label.text = str(self.score)

        # Game over
        if self.game_over:
            Clock.unschedule(self.start_game)
            self.canvas.clear()
            self.init_game()
            self.update_init_game()

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "up":
            self.movey = self.sizey
            self.movex = 0
        elif keycode[1] == "down":
            self.movey = -self.sizey
            self.movex = 0
        elif keycode[1] == "left":
            self.movex = -self.sizex
            self.movey = 0
        elif keycode[1] == "right":
            self.movex = self.sizex
            self.movey = 0
        return True


class SnakeParts(Widget):
    pass


class SnakeApp(App):
    pass


SnakeApp().run()
