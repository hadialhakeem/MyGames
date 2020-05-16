import pygame
import random

pygame.init()

# Set up room and variables
room_width = 900
room_height = 600
window = pygame.display.set_mode((room_width, room_height))
pygame.display.set_caption("GAME_NAME")

allobjs = []



class Text:
    colors = {'black': (0, 0, 0), 'blue': (0, 0, 255), 'beige': (207, 185, 151), 'white': (255, 255, 255),
              'yellow': (255, 255, 0), 'red': (255, 0, 0), 'gray': (192, 192, 192), 'lightblue': (13, 206, 250),
              'darkbrown': (185, 171, 158), 'lightbrown': (205, 193, 181)}

    bgcolor = colors['beige']

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
            box_colour = self.colors['gray']

            mbleft, mbmiddle, mbright = pygame.mouse.get_pressed()
            if mbleft:
                return True

        else:
            box_colour = self.colors['white']

        pygame.draw.rect(self.window, box_colour, [box_x, box_y, box_width, box_height])
        pygame.draw.rect(self.window, self.colors['black'], [box_x, box_y, box_width, box_height], 5)
        self.display(text, text_x, text_y, self.colors['black'], font)

    def create_border(self, x, y, width, height, thickness, colour):
        pygame.draw.rect(self.window, colour, (x, y, width, thickness))
        pygame.draw.rect(self.window, colour, (x, y, thickness, height))
        pygame.draw.rect(self.window, colour, (x + width - thickness, y, thickness, height))
        pygame.draw.rect(self.window, colour, (x, y + height - thickness, width, thickness))


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
            pygame.draw.rect(window, Text.colors['black'], [self.x, self.y, self.width, self.height], 2)



def draw_background():
    window.fill(Text.bgcolor)

def draw_paused():
    text.display("P A U S E D", room_width/2, room_height/2, Text.colors['white'], Text.largefont, "center")

def close():
    global paused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        #Pause Feature
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if paused:
                    paused = False
                else:
                    paused = True

def draw():
    for obj in allobjs:
        obj.draw()


text = Text(window)
paused = False

# Main Game loop
while True:
    close()
    draw_background()

    if not paused:
        draw()
    else:
        draw_paused()

    pygame.time.delay(1)
    pygame.display.update()
