import pyray
import pyray as pr
import random
import time
import numpy as np


class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 3 #зачем ?? я хз.(((
        self.status = {
            "moving": "none",
            "power-ups": [],
            "alive": True
        }
        self.score = 0

    def move(self, direction):
        if self.status["alive"]:
            if direction == "up":
                self.y -= 25
            elif direction == "down":
                self.y += 25
            elif direction == "left":
                self.x -= 30
            elif direction == "right":
                self.x += 30
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
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.status = {
            'moving': 'none',
            'alive': True,
            'mode': 'hunt'
        }
        self.cost = 200
        self.color = color

    def move(self, pacman, map_data, direction=None):
        if self.status["alive"]:
            new_x, new_y = self.x, self.y

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

            if abs(self.x - pacman.x) >= abs(self.y - pacman.y):
                if self.x >= pacman.x:
                    new_x -= 3
                else:
                    new_x += 3
            else:
                if self.y >= pacman.y:
                    new_y -= 3
                else:
                    new_y += 3
            if map_data[int(new_y // 25)][int(new_x // 30)] != "X":
                self.x, self.y = new_x, new_y
            self.status["moving"] = direction

    def draw(self):
        if self.status['alive']:
            pr.draw_circle(self.x, self.y, 10, self.color)

    def collide(self, pacman):
        if self.status['alive']:
            if (pacman.x - self.x) ** 2 + (pacman.y - self.y) ** 2 < 25 ** 2:
                pacman.status['alive'] = False
                print("YOU SUCK")


class Fruit:
    def __init__(self, x, y, points, time):
        self.x = x
        self.y = y
        self.points = points
        self.time =

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

def eat(fruits, pacman): #нужно
    for fruit in fruits[:]:
        if (pacman.x - fruit.x) ** 2 + (pacman.y - fruit.y) ** 2 < 25 ** 2:
            pacman.eat(fruit)
            fruit.eating()


map = [
    list("XXXXXXXXXXXXXXXXXXXXXXXXXXXX"),
    list("Xp    F      XX      F     X"),
    list("X XXXX XXXXX XX XXXXX XXXX X"),
    list("X XXXX XXXXX XX XXXXX XXXX X"),
    list("X XXXX XXXXX XX XXXXX XXXX X"),
    list("X     F              F     X"),
    list("X XXXX XX XXXXXXXX XX XXXX X"),
    list("X XXXX XX XXXXXXXX XX XXXX X"),
    list("X      XX    XX    XX      X"),
    list("XXXXXX XXXXX XX XXXXX XXXXXX"),
    list("XXXXXX XXXXX XX XXXXX XXXXXX"),
    list("XXXXXX XX          XX XXXXXX"),
    list("XXXXXX XX XXX  XXX XX XXXXXX"),
    list("XXXXXX XX X      X XX XXXXXX"),
    list("I     F   X  g g X   F     I"),
    list("XXXXXX XX X  g g X XX XXXXXX"),
    list("XXXXXX XX XXXXXXXX XX XXXXXX"),
    list("XXXXXX XX          XX XXXXXX"),
    list("XXXXXX XXXXX XX XXXXX XXXXXX"),
    list("XXXXXX XXXXX XX XXXXX XXXXXX"),
    list("X      XX    XX    XX      X"),
    list("X XXXX XX XXXXXXXX XX XXXX X"),
    list("X XXXX XX XXXXXXXX XX XXXX X"),
    list("X     F              F     X"),
    list("X XXXX XXXXX XX XXXXX XXXX X"),
    list("X XXXX XXXXX XX XXXXX XXXX X"),
    list("X XXXX XXXXX XX XXXXX XXXX X"),
    list("X     F      XX      F     X"),
    list("XXXXXXXXXXXXXXXXXXXXXXXXXXXX")

]

class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 30
        self.width = 25

    def draw(self):
        pr.draw_rectangle(
            self.x,
            self.y,
            self.height,
            self.width,
            pr.BLUE
        )
class Portal:
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
        pr.RED
        )

def teleportL(pacman):
    print('L', pacman.x, pacman.y)
    pacman.x = 765

def teleportR(pacman):
    print('R', pacman.x, pacman.y)
    pacman.x = 75

def draw_map(map_data, pacman):
    current_x, current_y = pacman.x, pacman.y
    for i in range(len(map_data)):
        for j in range(len(map_data[i])):
            if map_data[i][j] == "X":
                wall = Wall(j * 30, i * 25)
                wall.draw()
            if map_data[i][j] == "I":
                port = Portal(j * 30, i * 25)
                port.draww()
            if map_data[i][j] == "p":
                new_x, new_y = current_x, current_y
                if pr.is_key_down(pr.KeyboardKey.KEY_W):
                    new_y -= 25
                elif pr.is_key_down(pr.KeyboardKey.KEY_S):
                    new_y += 25
                elif pr.is_key_down(pr.KeyboardKey.KEY_A):
                    new_x -= 30
                elif pr.is_key_down(pr.KeyboardKey.KEY_D):
                    new_x += 30

                if map_data[int(new_y // 25)][int(new_x // 30)] not in ["X", "I"]:
                    pacman.x, pacman.y = new_x, new_y
                    map_data[i][j] = " "
                    map_data[int(new_y // 25)][int(new_x // 30)] = "p"
                else:
                    if pr.is_key_down(pr.KeyboardKey.KEY_W) and map_data[i - 1][j] not in ["X", "I"]:
                        new_y -= 25
                    elif pr.is_key_down(pr.KeyboardKey.KEY_S) and map_data[i + 1][j] not in ["X", "I"]:
                        new_y += 25
                    elif pr.is_key_down(pr.KeyboardKey.KEY_A) and map_data[i][j - 1] not in ["X", "I"]:
                        new_x -= 30
                    elif pr.is_key_down(pr.KeyboardKey.KEY_D) and map_data[i][j + 1] not in ["X", "I"]:
                        new_x += 30

                    if map_data[int(new_y // 25)][int(new_x // 30)] not in ["X", "I"]:
                        pacman.x, pacman.y = new_x, new_y
                        map_data[i][j] = " "
                        map_data[int(new_y // 25)][int(new_x // 30)] = "p"

                if map_data[i][j - 1] == 'I':
                    teleportL(pacman)
                elif map_data[i][j + 1] == 'I':
                    teleportR(pacman)



    #print(pacman.status['moving'])

def createe():
    pr.init_window(840, 725, "Pacman")
    pr.set_target_fps(10)
    pacman = Pacman(45, 37)
    fruits = [
        Seed(random.randrange(799), random.randrange(599)),
        Energizer(random.randrange(799), random.randrange(599)),
        Cherry(random.randrange(799), random.randrange(599))
    ]
    ghost= []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 'g':
                ghost.append((j * 30 + 15, i * 25 + 15))
    ghost = [
        Ghost(x, y, pyray.GREEN) for (x, y) in ghost
    ]
    return fruits, pacman, ghost

def GhostUpdate(ghosts, pacman, map_data):
    for ghost in ghosts:
        ghost.move(pacman, map_data)
        ghost.draw()
    for ghost in ghosts:
        ghost.collide(pacman)


def main():
    fruits, pacman, ghosts = createe()
    frames=0
    while not pr.window_should_close():
        playing=pacman.status['alive']
        frames+=1
        draw_map(map, pacman)
        if playing:
            GhostUpdate(ghosts, pacman, map)
        else:
            if (frames//30)%2:
                pr.draw_text('GAME OVER', 200, 200, 75, pr.RED)
            pr.draw_text('Better luck next time!', 220, 500, 35, pr.RAYWHITE)
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        pacman.draw()
        pr.draw_text(f"Score: {pacman.score}", 10, 10, 20, pr.WHITE)
        pr.end_drawing()

    pr.close_window()



if __name__ == '__main__':
    main()
