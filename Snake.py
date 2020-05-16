import pygame
import random

pygame.init()

# Set up room and variables
room_width = 800
room_height = 900
window = pygame.display.set_mode((room_width, room_height))
pygame.display.set_caption("Snake")

allobjs = []

# RGB Colors
black = (0, 0, 0)
blue = (0, 0, 255)
beige = (207, 185, 151)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
gray = (192, 192, 192)
lightblue = (13, 206, 250)
darkbrown = (185, 171, 158)
lightbrown = (205, 193, 181)
bgcolor = black

class Text:
    # Set up fonts
    hugefont = pygame.font.SysFont("Times New Roman", 170)
    largefont = pygame.font.SysFont("Times New Roman", 120)
    mediumfont = pygame.font.SysFont("Times New Roman", 85)
    smallfont = pygame.font.SysFont("Times New Roman", 55)
    textfont = pygame.font.SysFont("Times New Roman", 30)

    def __init__(self, window):
        self.buttonpadding = 20
        self.window = window

    def display(self, text, x, y, color, font, alignment="left"):
        # In pygame you have to render the font, then blit it onto a screen.
        # This is what is done here.
        if alignment == "center":
            text_width, text_height = font.size(text)
            text_x = x - (text_width / 2)
            text_y = y
        else:
            text_x = x
            text_y = y
            if alignment != "left":
                print("Invalid Alignment. Choose 'left' or 'center'. Defaulted to left")

        render = font.render(text, 0, color)
        self.window.blit(render, (text_x, text_y))

    def create_button(self, text, x, y, font, alignment = "left"):
        text_width, text_height = font.size(text)

        box_width = text_width + self.buttonpadding
        box_height = text_height + self.buttonpadding

        if alignment == "center":
            box_x = x - (box_width / 2)
            box_y = y - (box_height / 2)

        else:
            box_x = x
            box_y = y

            if alignment != 'left':
                print("Invalid Alignment. Choose 'left' or 'center'. Deafulted to left")


        text_x = box_x + (self.buttonpadding / 2)
        text_y = box_y + (self.buttonpadding / 2)

        mx, my = pygame.mouse.get_pos()

        if box_x < mx < box_x + box_width and box_y < my < box_y + box_height:
            box_colour = gray

            mbleft, mbmiddle, mbright = pygame.mouse.get_pressed()
            if mbleft:
                return True

        else:
            box_colour = white

        pygame.draw.rect(self.window, box_colour, [box_x, box_y, box_width, box_height])
        pygame.draw.rect(self.window, black, [box_x, box_y, box_width, box_height], 5)
        self.display(text, text_x, text_y, black, font)

    def create_border(self, x, y, width, height, thickness, colour):
        pygame.draw.rect(self.window, colour, (x, y, width, thickness))
        pygame.draw.rect(self.window, colour, (x, y, thickness, height))
        pygame.draw.rect(self.window, colour, (x + width - thickness, y, thickness, height))
        pygame.draw.rect(self.window, colour, (x, y + height - thickness, width, thickness))


class Snake:
    tile_length = 40
    game_width = 20
    game_height = game_width
    game_padding = room_height - (game_height * tile_length)
    border_thickness = 3
    score = 0

    def __init__(self, screen):
        self.window = screen
        x = Snake.game_width // 4
        y = Snake.game_height // 2
        self.dir = 0
        # Directions
        # 0 - Right
        # 1 - Up
        # 2 - Left
        # 3 - Down

        self.pos = [(x, y),
                    (x - 1, y),
                    (x - 2, y)]

        self.foodeaten = False
        self.timer = 0
        self.action = False
        self.border = Text(self.window)
        self.maxtimer = 100

        allobjs.append(self)

    def getinput(self):
        keys = pygame.key.get_pressed()
        if self.dir == 0 or self.dir == 2:
            if keys[pygame.K_UP]:
                self.dir = 1
                self.action = True

            if keys[pygame.K_DOWN]:
                self.dir = 3
                self.action = True
        else:
            if keys[pygame.K_RIGHT]:
                self.dir = 0
                self.action = True

            if keys[pygame.K_LEFT]:
                self.dir = 2
                self.action = True

    def collision_food(self, foodobj):
        if self.pos[0] == foodobj.pos:
            foodobj.pos = foodobj.newpos()
            Snake.score += 1
            self.foodeaten = True

    def collision_self(self):
        headpos = self.pos[0]
        bodypos = self.pos[1:]

        for body in bodypos:
            if headpos == body:
                print("YOU LOST")
                pygame.quit()
                quit()

    def collision_wall(self):
        headposx = self.pos[0][0]
        headposy = self.pos[0][1]

        if headposx < 1 or headposx > Snake.game_width or headposy < 1 or headposy > Snake.game_height:
            print("YOU LOST")
            pygame.quit()
            quit()

    # This is what happens every frame
    def update(self, food):
        if not self.action:
            self.getinput()

        self.timer += 1
        if self.timer > self.maxtimer:
            self.maxtimer = 100 - (10*(Snake.score // 10))
            self.action = False
            self.timer = 0

            # Move the snake in it's direction
            if self.dir == 0:
                newpos = (self.pos[0][0] + 1, self.pos[0][1])

            elif self.dir == 1:
                newpos = (self.pos[0][0], self.pos[0][1] - 1)

            elif self.dir == 2:
                newpos = (self.pos[0][0] - 1, self.pos[0][1])

            else:
                newpos = (self.pos[0][0], self.pos[0][1] + 1)

                if self.dir != 3:
                    print("Error in Snake direction. This should never happen.")

            self.pos = self.shiftlist(self.pos, newpos, self.foodeaten)
            self.foodeaten = False

            # Check for all collisions
            self.collision_food(food)
            self.collision_self()
            self.collision_wall()


    @staticmethod
    def shiftlist(inputlist, newitem, food):
        newlist = [newitem]
        newlist += inputlist

        if not food:
            newlist = newlist[:-1]

        return newlist

    def draw(self):
        for square in self.pos:
            x = (square[0] - 1) * Snake.tile_length
            y = (square[1] - 1) * Snake.tile_length + Snake.game_padding
            pos = (x, y, Snake.tile_length, Snake.tile_length)
            pygame.draw.rect(self.window, white, pos)
            self.border.create_border(x, y, Snake.tile_length, Snake.tile_length, Snake.border_thickness, gray)


class Food:
    def __init__(self, window, snakeobj):
        self.window = window
        self.snake = snakeobj
        self.pos = self.newpos()

        allobjs.append(self)

    def newpos(self):
        run = True
        while run:
            x = random.randint(1, Snake.game_width)
            y = random.randint(1, Snake.game_height)

            run = False
            for squarepos in self.snake.pos:
                if (x, y) == squarepos:
                    run = True

        return x, y

    def draw(self):
        x = (self.pos[0] - 1) * Snake.tile_length
        y = (self.pos[1] - 1) * Snake.tile_length + Snake.game_padding
        rect = (x, y, Snake.tile_length, Snake.tile_length)
        pygame.draw.rect(self.window, blue, rect)



def draw_background():
    window.fill(bgcolor)
    pygame.draw.line(window, white, (0, Snake.game_padding - 1), (room_width, Snake.game_padding - 1))

def draw_paused():
    text.display("P A U S E D", room_width/2, room_height/2, white, Text.largefont, "center")

def close():
    global paused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if paused:
                    paused = False
                else:
                    paused = True

def draw():
    for obj in allobjs:
        obj.draw()


snake = Snake(window)
food = Food(window, snake)
text = Text(window)
paused = False

while True:
    close()
    draw_background()
    text.display("Score: " + str(Snake.score), room_width / 2, 5, white, text.mediumfont, "center")

    if not paused:
        draw()
        snake.update(food)
    else:
        draw_paused()

    pygame.time.delay(1)
    pygame.display.update()
