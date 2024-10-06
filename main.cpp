import pyray as pr
import random
import time

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 3
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
            pr.draw_circle(self.x, self.y, 20, pr.YELLOW)

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


def FruitDraw(fruits):
    for fruit in fruits:
        fruit.draw()


def eat(fruits, pacman):
    for fruit in fruits[:]:
        if (pacman.x - fruit.x) ** 2 + (pacman.y - fruit.y) ** 2 < 25 ** 2:
            pacman.eat(fruit)
            fruit.eating()


def movee(pacman):
    if pr.is_key_down(pr.KEY_UP):
        pacman.move("up")
    elif pr.is_key_down(pr.KEY_DOWN):
        pacman.move("down")
    elif pr.is_key_down(pr.KEY_LEFT):
        pacman.move("left")
    elif pr.is_key_down(pr.KEY_RIGHT):
        pacman.move("right")

def createe():
    pr.init_window(800, 600, "Pacman")
    pr.set_target_fps(60)
    pacman = Pacman(400, 300)
    fruits = [
        Seed(random.randrange(799), random.randrange(599)),
        Energizer(random.randrange(799), random.randrange(599)),
        Cherry(random.randrange(799), random.randrange(599))
    ]
    return fruits, pacman

def main():
    fruits, pacman = createe()
    while not pr.window_should_close():
        movee(pacman)
        eat(fruits, pacman)
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        pacman.draw()
        FruitDraw(fruits)
        pr.draw_text(f"Score: {pacman.score}", 10, 10, 20, pr.WHITE)
        pr.end_drawing()

    pr.close_window()



if __name__ == '__main__':
    main()
