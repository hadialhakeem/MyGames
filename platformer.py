import pygame
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
        self.interact = True

        allobjs.append(self)

    def draw(self):
        if self.interact:
            pygame.draw.rect(window, self.colour, [self.x, self.y, self.width, self.height])

            if self.border:
                pygame.draw.rect(window, black, [self.x, self.y, self.width, self.height], 2)

    def hide(self):
        self.interact = False

    def show(self):
        self.interact = True

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


class Player(Base):
    def __init__(self, x, y, width, height, colour):
        Base.__init__(self, x, y, width, height, colour)
        self.hsp = 0
        self.vsp = 0
        self.friction = 0.93
        self.jumpspeed = -12
        self.accel = 0.2
        self.maxspeed = 5
        self.jump = False
        self.lives = 3

    def get_inputs(self):
        keys = pygame.key.get_pressed()
        direction = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])

        if direction == 0:
            self.hsp *= self.friction

        elif abs(self.hsp + (self.accel * direction)) < self.maxspeed:
            self.hsp += (self.accel * direction)

        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
            if self.jump:
                self.vsp = self.jumpspeed

    def apply_gravity(self):
        onfloor = False
        for icounter in range(Object.inits):
            if self.place_meeting(self.x, self.y + 1, Object.attributes[icounter]):
                onfloor = True

        if onfloor:
            self.jump = True
        else:
            self.jump = False
            if self.vsp < maxgrav:
                self.vsp += gravity

    def place_meeting(self, x, y, obj):
        if (x + self.width > obj.x and x < obj.x + obj.width) and (y + self.height > obj.y and y < obj.y + obj.height) and obj.interact:
            return True
        else:
            return False

    def reset_player(self):
        self.x = 100
        self.y = Object.attributes[0].y - self.height - 20
        self.vsp = 0
        self.hsp = 0

    def collision_objects(self):
        for icounter in range(Object.inits):
            #Horizontal collision checking
            if self.place_meeting(self.x + self.hsp, self.y, Object.attributes[icounter]):
                if self.hsp > 0:
                    self.x = Object.attributes[icounter].x - self.width
                else:
                    self.x = Object.attributes[icounter].x + Object.attributes[icounter].width

                self.hsp = 0

            # Verical collision checking
            if self.place_meeting(self.x, self.y + self.vsp, Object.attributes[icounter]):
                if self.vsp > 0:
                    self.y = Object.attributes[icounter].y - self.height
                else:
                    self.y = Object.attributes[icounter].y + Object.attributes[icounter].height

                self.vsp = 0

    def collision_door(self, door_instance):
        if self.place_meeting(self.x, self.y, door_instance):
            global level
            level += 1
            self.reset_player()

            if level == 2:
                lava.show()
            elif level == 3:
                lava.width *= 3
                lava.x -= 100
                platform2.show()

    def collision_lava(self, lava_instance):
        if self.place_meeting(self.x, self.y, lava_instance):
            self.lives -= 1
            if self.lives == 0:
                pygame.quit()
                quit()

            self.reset_player()

    def apply_movement(self):
        self.x += self.hsp
        self.y += self.vsp


class Text:
    # Set up fonts
    hugefont = pygame.font.SysFont("Times New Roman", 170)
    largefont = pygame.font.SysFont("Times New Roman", 120)
    mediumfont = pygame.font.SysFont("Times New Roman", 85)
    smallfont = pygame.font.SysFont("Times New Roman", 55)
    textfont = pygame.font.SysFont("Times New Roman", 30)

    def __init__(self, window):
        self.textlevel = 0
        self.buttonpadding = 30

        self.window = window

    def display(self, text, x, y, color, font, alignment="left"):
        # In pygame you have to render the font, then blit it onto a screen.
        # This is what is done here.

        global level
        if level == self.textlevel or self.textlevel == 0:
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


def close():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

def draw():
    # Draw all Objects
    for icounter in range(len(allobjs)):
        allobjs[icounter].draw()


# Set up room and variables
room_width = 1200
room_height = 800
window = pygame.display.set_mode((room_width, room_height))
pygame.display.set_caption("Platformer")

# Set up player variables
playerx = 100
playery = 150
playerwidth = 50

# Set up deafult platform variables
platform_height = 20
platform_width = 200

#World Variables
level = 1
gravity = 0.25
maxgrav = 20

# RGB Colors
black = (0, 0, 0)
blue = (0, 0, 255)
beige = (207, 185, 151)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
gray = (192, 192, 192)

text = Text(window)
#---------Main Menu-------------
run = True
while run:
    # Clear Screen
    window.fill(beige)
    close()

    text.display("My Platformer", room_width / 2, 20, blue, text.hugefont, "center")
    if text.create_button("Start", room_width/2, room_height/2, text.hugefont, "center"):
        run = False

    pygame.display.update()
    pygame.time.delay(1)

#-------------------------------
#----Initialize all Objects-----
# Init player object
player = Player(playerx, playery, playerwidth, playerwidth, blue)

# These are permanent objects which will never change
# Floor
Object(0, 700, room_width, 100, black)
# Left Wall
Object(0, 0, 50, room_height, black)
# Right Wall
Object(room_width - 50, 0, 50, room_height, black)

platform1 = Object(20, room_height/2 + 50, platform_width, platform_height, black)
platform2 = Object(500, room_height/2 + 50, platform_width, platform_height, black)

door = Base(room_width - 110, 650, 30, 30, yellow)
door.border = True

lava = Base(400, 699, 200, 100, red)

# Initialize Level 1
platform1.hide()
platform2.hide()
lava.hide()

run = True
while True:
    # Clear Screen
    window.fill(beige)
    close()

    #---This section handles text prints--------
    # Text to be displayed at all times
    text.textlevel = 0
    text.display("Level " + str(level), 100, 10, black, text.mediumfont)
    text.display("Lives: " + str(player.lives), 110, 100, black, text.smallfont)

    # Level 1 text
    text.textlevel = 1
    text.display("Move with arrow keys or WASD", 200, 200, black, text.smallfont)

    # Level 2 text
    text.textlevel = 2
    text.display("Don't touch the lava", 200, 200, black, text.smallfont)

    # Level 3 text
    text.textlevel = 3
    text.display("Use the platform", 200, 200, black, text.smallfont)

    # Level 4 text
    text.textlevel = 4
    text.display("Well... that's it for now", 200, 200, black, text.smallfont)

    # Level 5 text
    text.textlevel = 5
    text.display("You're still here?", 200, 200, black, text.smallfont)

    # Level 6 text
    text.textlevel = 6
    text.display("You realize there's nothing more right...", 200, 200, black, text.smallfont)

    # Level 7 text
    text.textlevel = 7
    text.display("...", 200, 200, black, text.smallfont)

    # Level 8 text
    text.textlevel = 8
    text.display("Well have fun", 200, 200, black, text.smallfont)

    # Level 10 text
    text.textlevel = 10
    text.display("Just don't die", 200, 200, black, text.smallfont)
    #-------------------------------------------

    #---This section handles all game objects---
    player.get_inputs()
    player.apply_gravity()
    player.collision_objects()
    player.collision_door(door)
    player.collision_lava(lava)
    player.apply_movement()

    draw()

    #-------------------------------------------
    pygame.display.update()
    pygame.time.delay(5)

