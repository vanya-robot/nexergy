import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

class Snake(Widget):
    # define the properties of the snake
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # move the snake by updating its position
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class Food(Widget):
    # create the food at a random position
    def create_food(self):
        self.pos = (randint(0, self.parent.width-self.width), randint(0, self.parent.height-self.height))

class SnakeGame(Widget):
    snake = Snake()
    food = Food()

    # initialize the game by creating the snake and food
    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self.snake.pos = (self.width/2, self.height/2)
        self.add_widget(self.snake)
        self.add_widget(self.food)
        self.food.create_food()
        Clock.schedule_interval(self.update, 1.0/10.0)

    # update the game by moving the snake and checking for collisions
    def update(self, *args):
        self.snake.move()
        self.check_collision()

    # check for collisions with the wall and the food
    def check_collision(self):
        # check for collision with the wall
        if (self.snake.x < 0) or (self.snake.x + self.snake.width > self.width) or (self.snake.y < 0) or (self.snake.y + self.snake.height > self.height):
            self.game_over()
        # check for collision with the food
        if self.snake.collide_widget(self.food):
            self.food.create_food()
            self.snake.velocity = Vector(*self.snake.velocity).rotate(randint(-45,45))

    # end the game and restart
    def game_over(self):
        self.snake.pos = (self.width/2, self.height/2)
        self.snake.velocity = (0, 0)

class SnakeApp(App):
    def build(self):
        return SnakeGame()

if __name__ == '__main__':
    SnakeApp().run()