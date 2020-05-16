import pygame
from random import randint

pygame.init()

allobjs = []

class Base:
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.border = False

        allobjs.append(self)

    def draw(self):
        pygame.draw.rect(window, self.colour, [self.x, self.y, self.width, self.height])

        if self.border:
            pygame.draw.rect(window, black, [self.x, self.y, self.width, self.height], 2)


class Object(Base):
    inits = 0
    attributes = []

    def __init__(self, x, y, width, height, colour):
        Base.__init__(self, x, y, width, height, colour)
        Object.inits += 1
        Object.attributes.append(self)

    def delete(self):
        allobjs.remove(self)
        Object.inits -= 1
        Object.attributes.remove(self)


class Circle:
    def __init__(self, x, y, radius, colour, screen):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.window = screen

        self.border = False
        allobjs.append(self)

    def place_meeting(self, x, y, obj, objtype):
        if objtype == "obj":
            if (x + self.radius > obj.x and x - self.radius < obj.x + obj.width) and (y + self.radius > obj.y and y - self.radius < obj.y + obj.height):
                return True
            else:
                return False
        else:
            if (x + self.radius > obj.x - obj.radius and x - self.radius < obj.x + obj.radius) and (y + self.radius > obj.y - obj.radius and y - self.radius < obj.y + obj.radius):
                return True
            else:
                return False

    def draw(self):
        pygame.draw.circle(self.window, self.colour, [self.x, self.y], self.radius)

        if self.border:
            pygame.draw.circle(self.window, black, [self.x, self.y], self.radius, 2)


class Enemy(Circle):
    enemies = []
    radius = 12

    def __init__(self, x, y, screen):
        self.radius = Enemy.radius
        self.colour = red
        Circle.__init__(self, x, y, self.radius, self.colour, screen)

        self.xory = randint(0, 1)
        # 0 - Horizontal
        # 1 - Vertical

        randomnum = randint(0, 1)
        if randomnum == 0:
            self.dir = -1
        else:
            self.dir = 1

        self.speed = 3
        Enemy.enemies.append(self)

    def move(self):
        if self.xory == 0:
            self.x += self.dir * self.speed
        else:
            self.y += self.dir * self.speed

    def collision(self):
        # Collision with the wall
        for icounter in range(Object.inits):
            if self.place_meeting(self.x, self.y, Object.attributes[icounter], "obj"):
                self.dir *= -1

    def delete(self):
        allobjs.remove(self)
        Enemy.enemies.remove(self)


class Player(Circle):
    def __init__(self, x, y, screen):
        self.radius = 35
        self.colour = black
        Circle.__init__(self, x, y, self.radius, self.colour, screen)

        self.hsp = 0
        self.vsp = 0
        self.accel = 0.3
        self.maxspeed = 5
        self.invincible_iterations = 50000
        self.invincible_dots = 7
        self.counter = 0

        self.invincible = False

    def get_inputs(self):
        keys = pygame.key.get_pressed()
        h_direction = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        v_direction = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])

        if h_direction == 0:
            if abs(self.hsp) > self.accel:
                self.hsp += self.accel * -sign(self.hsp)
            else:
                self.hsp = 0

        elif abs(self.hsp + (self.accel * h_direction)) < self.maxspeed:
            self.hsp += (self.accel * h_direction)

        if v_direction == 0:
            if abs(self.vsp) > self.accel:
                self.vsp += self.accel * -sign(self.vsp)
            else:
                self.vsp = 0

        elif abs(self.vsp + (self.accel * v_direction)) < self.maxspeed:
            self.vsp += (self.accel * v_direction)

    def collision(self):
        # ---Collision With Border
        for icounter in range(Object.inits):
            #Horizontal Collision Checking
            if self.place_meeting(self.x + self.hsp, self.y, Object.attributes[icounter], "obj"):
                if self.hsp > 0:
                    self.x = Object.attributes[icounter].x - self.radius
                else:
                    self.x = Object.attributes[icounter].x + Object.attributes[icounter].width + self.radius

                self.hsp = 0

            # Verical collision checking
            if self.place_meeting(self.x, self.y + self.vsp, Object.attributes[icounter], "obj"):
                if self.vsp > 0:
                    self.y = Object.attributes[icounter].y - self.radius
                else:
                    self.y = Object.attributes[icounter].y + Object.attributes[icounter].height + self.radius

                self.vsp = 0

        # ---Collision with Enemies
        for icounter in range(len(Enemy.enemies)):
            if self.place_meeting(self.x, self.y, Enemy.enemies[icounter], "circle"):
                #if self.invincible:
                 #   Enemy.enemies[icounter].delete()
                #else:
                    return True

    def collision_food(self, food_obj):
        if self.place_meeting(self.x, self.y, food_obj, "circle"):
            global score
            score += 1
            food_obj.x = randint(border_thickness + food_obj.radius, border_width - border_thickness - food_obj.radius)
            food_obj.y = randint(border_yoffset + border_thickness + food_obj.radius, room_height - border_thickness - food_obj.radius)

            # Quadrants:
            # 2 1
            # 3 4
            # Enemy quadrant must be diagonally opposite the player.

            if self.x > room_width/2:
                if self.y > border_yoffset + (border_height/2):
                    enemy_quadrant = 2
                else:
                    enemy_quadrant = 3
            else:
                if self.y > border_yoffset + (border_height/2):
                    enemy_quadrant = 1
                else:
                    enemy_quadrant = 4

            if enemy_quadrant == 1:
                enemy_x = randint(border_width / 2, border_width - border_thickness - Enemy.radius)
                enemy_y = randint(border_thickness + border_yoffset + Enemy.radius, border_yoffset + (border_height/2))

            elif enemy_quadrant == 2:
                enemy_x = randint(border_thickness + Enemy.radius, border_width / 2)
                enemy_y = randint(border_thickness + border_yoffset + Enemy.radius, border_yoffset + (border_height/2))

            elif enemy_quadrant == 3:
                enemy_x = randint(border_thickness + Enemy.radius, border_width / 2)
                enemy_y = randint(border_yoffset + (border_height/2), room_height - border_thickness - Enemy.radius)

            else:
                enemy_x = randint(border_width / 2, border_width - border_thickness - Enemy.radius)
                enemy_y = randint(border_yoffset + (border_height / 2), room_height - border_thickness - Enemy.radius)

            Enemy(enemy_x, enemy_y, self.window)

    def apply_movement(self):
        self.x += round(self.hsp)
        self.y += round(self.vsp)

    def draw(self):
        pygame.draw.circle(self.window, self.colour, [self.x, self.y], self.radius)



        if self.border:
            pygame.draw.circle(self.window, black, [self.x, self.y], self.radius, 2)


class Text:
    # Set up fonts
    hugefont = pygame.font.SysFont("Times New Roman", 170)
    largefont = pygame.font.SysFont("Times New Roman", 120)
    mediumfont = pygame.font.SysFont("Times New Roman", 85)
    smallfont = pygame.font.SysFont("Times New Roman", 55)
    textfont = pygame.font.SysFont("Times New Roman", 30)

    def __init__(self, window):
        self.textlevel = 0
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

        if alignment == "left":
            box_x = x
            box_y = y

        elif alignment == "center":
            box_x = x - (box_width/2)
            box_y = y - (box_height/2)

        else:
            print("Invalid Alignment. Choose 'left' or 'center'")
            return False

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


def draw():
    # Draw all Objects
    for icounter in range(len(allobjs)):
        allobjs[icounter].draw()


def enemy_actions():
    for icounter in range(len(Enemy.enemies)):
        Enemy.enemies[icounter].move()
        Enemy.enemies[icounter].collision()


def reset():
    global score
    global player

    player.hsp = 0
    player.vsp = 0
    player.x = room_width // 2
    player.y = room_height // 2

    score = 0

    iterations = len(Enemy.enemies)
    for icounter in range(iterations):
        Enemy.enemies[0].delete()


def close():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


def sign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0


def create_border(x, y, width, height, thickness, colour):
    Object(x, y, width, thickness, colour)
    Object(x, y, thickness, height, colour)
    Object(x + width - thickness, y, thickness, height, colour)
    Object(x, y + height - thickness, width, thickness, colour)

def draw_bar(x, y, width, height, colour, input, max):
    percentage = input / max
    bar_width = percentage * width
    b_width = 10

    pygame.draw.rect(window, black, [x - b_width, y - b_width, width + b_width, b_width])
    pygame.draw.rect(window, black, [x - b_width, y - b_width, b_width, height + b_width])
    pygame.draw.rect(window, black, [x - b_width, y + height, width + b_width, b_width])
    pygame.draw.rect(window, black, [x + width, y - b_width, b_width, height + b_width + b_width])

    if percentage != 0:
        pygame.draw.rect(window, colour, [x, y, bar_width, height])


# RGB Colors
black = (0, 0, 0)
blue = (0, 0, 255)
beige = (207, 185, 151)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
gray = (192, 192, 192)
lightblue = (13, 206, 250)

bgcolor = beige

# Set up room and variables
room_width = 1000
room_height = 800
window = pygame.display.set_mode((room_width, room_height))
pygame.display.set_caption("Dots")

# Food Variables
food_colour = blue
food_radius = Enemy.radius

# Global Variables
score = 0

text = Text(window)

player = Player(room_width // 2, room_height // 2, window)
food = Circle(400, 400, food_radius, food_colour, window)

# Border Variables
border_thickness = 20
border_yoffset = 100
border_height = room_height - border_yoffset
border_width = room_width

create_border(0, border_yoffset, border_width, border_height, border_thickness, black)

while True:
    run = True
    while run:
        window.fill(bgcolor)
        close()

        text.display("D O T S", room_width / 2, 20, black, Text.hugefont, "center")
        if text.create_button("Start", room_width / 2, room_height / 2 - 50, Text.largefont, "center"):
            run = False

        pygame.display.update()
        pygame.time.delay(5)

    reset()
    run = True
    invincible_iterations = 0
    while run:
        window.fill(bgcolor)
        close()

        text.display("Score: " + str(score), 20, 0, black, text.mediumfont)

        draw_bar(room_width / 2 - 50, 20, room_width / 2, border_yoffset - 50, lightblue, score % player.invincible_dots, player.invincible_dots)

        if score % player.invincible_dots == 0:
            player.invincible = True
            invincible_iterations = 0

        player.get_inputs()
        if player.collision():
            run = False

        player.collision_food(food)
        player.apply_movement()

        enemy_actions()

        draw()

        if player.invincible:
            invincible_iterations += 1

        if invincible_iterations > player.invincible_iterations:
            player.invincible = False

        pygame.display.update()
        pygame.time.delay(5)

    run = True
    while run:
        window.fill(bgcolor)
        close()

        text.display("You Died", room_width / 2, room_height / 2 - 200, black, text.largefont, "center")
        text.display("Your Score was: " + str(score), room_width / 2, room_height / 2 - 50, black, text.mediumfont, "center")

        if text.create_button("Play Again", room_width / 2, room_height / 2 + 150, Text.mediumfont, "center"):
            run = False

        if text.create_button("Quit", room_width / 2, room_height / 2 + 300, Text.mediumfont, "center"):
            pygame.quit()
            quit()

        pygame.display.update()
        pygame.time.delay(5)
