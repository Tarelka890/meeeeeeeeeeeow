import pyray
import pyray as pr
import random
import time
import numpy as np


class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 3 #зачем ??
        self.status = {
            "moving": "none",
            "power-ups": [],
            "alive": True
        }
        self.score = 0

    def move(self, direction):
        if self.status["alive"]:
            if direction == "up":
                self.y -= 5
            elif direction == "down":
                self.y += 5
            elif direction == "left":
                self.x -= 5
            elif direction == "right":
                self.x += 5
            self.status["moving"] = direction

    def eat(self, fruit):
        self.score += fruit.points
        if isinstance(fruit, Energizer):
            self.status["power-ups"].append("fear")

    def draw(self):
        if self.status["alive"]:
            pr.draw_circle(self.x, self.y, 10, pr.YELLOW)
            pr.draw_circle(self.x, self.y, 10, pr.YELLOW)

class Ghost():
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.status={
            'moving':'none',
            'alive':True,
            'mode':'hunt'
        }
        self.cost=200
        self.color=color

    def move(self, pacman):
        if self.status["alive"]:

            # ЭТОТ ВАРИАНТ РАБОАЕТ НАОБОРОТ, МОЖНО ИСПОЛЬЗОВАТЬ ДЛЯ МЕХАНИКИ FEAR

            # if abs(self.x-pacman.x) >= abs(self.y-pacman.y):
            #     if self.x >= pacman.x:
            #         self.x-=3
            #         direction = 'left'
            #     else:
            #         self.x+=3
            #         direction = 'right'
            # else:
            #     if self.y >= pacman.y:
            #         self.y+=3
            #         direction='down'
            #     else:
            #         self.y-=3
            #         direction='up'


            if abs(self.x-pacman.x) >= abs(self.y-pacman.y):
                if self.x >= pacman.x:
                    self.x-=3
                    direction = 'left'
                else:
                    self.x+=3
                    direction = 'right'
            else:
                if self.y >= pacman.y:
                    self.y-=3
                    direction='down'
                else:
                    self.y+=3
                    direction='up'
            self.status["moving"] = direction

    def draw(self):
        if self.status['alive']:
            pr.draw_circle(self.x, self.y, 20, self.color)


    def collide(self, pacman):
        if self.status['alive']:
            if (pacman.x - self.x) ** 2 + (pacman.y - self.y) ** 2 < 25 ** 2:
                pacman.status['alive']=False
                print("YOU SUCK")


class Fruit:
    def __init__(self, x, y, points):
        self.x = x
        self.y = y
        self.points = points

    def eating(self):
        self.x = random.randrange(799)
        self.y = random.randrange(599)

    def draw(self):
        raise NotImplementedError()

class Seed(Fruit):
    def __init__(self, x, y):
        super().__init__(x, y, 10)


    def draw(self):
        pr.draw_circle(self.x, self.y, 5, pr.BROWN)

class Energizer(Fruit):
    def __init__(self, x, y):
        super().__init__(x, y, 50)


    def draw(self):
        pr.draw_circle(self.x, self.y, 10, pr.BLUE)

class Cherry(Fruit):
    def __init__(self, x, y):
        super().__init__(x, y, 100)

    def draw(self):
        pr.draw_circle(self.x, self.y, 8, pr.RED)


map = [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "X            XX            X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X                          X",
            "X XXXX XX XXXXXXXX XX XXXX X",
            "X XXXX XX XXXXXXXX XX XXXX X",
            "X      XX    XX    XX      X",
            "XXXXXX XXXXX XX XXXXX XXXXXX",
            "XXXXXX XXXXX XX XXXXX XXXXXX",
            "XXXXXX XX    p     XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "XXXXXX XX X      X XX XXXXXX",
            "          X      X          ",
            "XXXXXX XX X      X XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "XXXXXX XX          XX XXXXXX",
            "XXXXXX XXXXX XX XXXXX XXXXXX",
            "XXXXXX XXXXX XX XXXXX XXXXXX",
            "X      XX    XX    XX      X",
            "X XXXX XX XXXXXXXX XX XXXX X",
            "X XXXX XX XXXXXXXX XX XXXX X",
            "X                          X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X            XX            X",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        ]

class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 30
        self.width = 25

    def draww(self):
        pr.draw_rectangle(
            self.x,
            self.y,
            self.height,
            self.width,
            pr.BLUE
        )

def draw_map(map_data):
    for y, row in enumerate(map_data):
        for x, char in enumerate(row):
            if char == "X":
                wall = Wall(x * 30, y * 25)
                wall.draww()

def FruitDraw(fruits):
    for fruit in fruits:
        fruit.draw()

def GhostUpdate(ghosts,pacman):
    for ghost in ghosts:
        ghost.draw()
    for ghost in ghosts:
        ghost.collide(pacman)
    for ghost in ghosts:
        ghost.move(pacman)


def eat(fruits, pacman):
    for fruit in fruits[:]:
        if (pacman.x - fruit.x) ** 2 + (pacman.y - fruit.y) ** 2 < 25 ** 2:
            pacman.eat(fruit)
            fruit.eating()


def movee(pacman):
    if pr.is_key_down(pr.KeyboardKey.KEY_W):
        pacman.move("up")
    elif pr.is_key_down(pr.KeyboardKey.KEY_S):
        pacman.move("down")
    elif pr.is_key_down(pr.KeyboardKey.KEY_A):
        pacman.move("left")
    elif pr.is_key_down(pr.KeyboardKey.KEY_D):
        pacman.move("right")
    else:
        pacman.move('none')

    #print(pacman.status['moving'])

def createe():
    pr.init_window(840, 840, "Pacman")
    pr.set_target_fps(60)
    pacman = Pacman(400, 287)
    fruits = [
        Seed(random.randrange(799), random.randrange(599)),
        Energizer(random.randrange(799), random.randrange(599)),
        Cherry(random.randrange(799), random.randrange(599))
    ]
    ghosts=[
        Ghost(700, 200, pyray.GREEN),
        Ghost(700, 300, pyray.ORANGE),
        Ghost(600, 150, pyray.PINK),
        Ghost(500, 400, pyray.SKYBLUE),
    ]
    return fruits, pacman, ghosts

def main():
    fruits, pacman, ghosts = createe()
    frames=0
    while not pr.window_should_close():
        playing=pacman.status['alive']
        frames+=1
        if playing:
            movee(pacman)
            GhostUpdate(ghosts, pacman)
            eat(fruits, pacman)
        else:
            if (frames//30)%2:
                pr.draw_text('GAME OVER', 200, 200, 75, pr.RED)
            pr.draw_text('Better luck next time!', 220, 500, 35, pr.RAYWHITE)
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        pacman.draw()
        FruitDraw(fruits)
        pr.draw_text(f"Score: {pacman.score}", 10, 10, 20, pr.WHITE)
        pr.end_drawing()

    pr.close_window()



if __name__ == '__main__':
    main()
