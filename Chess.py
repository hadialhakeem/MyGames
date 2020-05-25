import pygame

pygame.init()

# Set up room and variables
room_width = 800
room_height = 800
window = pygame.display.set_mode((room_width, room_height))
pygame.display.set_caption("Chess")

allobjs = []

paused = False
pressed = False

class Text:
    colors = {'black': (0, 0, 0), 'blue': (0, 0, 255), 'beige': (207, 185, 151), 'white': (255, 255, 255),
              'yellow': (255, 255, 0), 'red': (255, 0, 0), 'gray': (192, 192, 192), 'lightblue': (13, 206, 250),
              'darkbrown': (185, 171, 158), 'lightbrown': (205, 193, 181)}

    bgcolor = colors['beige']

    # Set up fonts
    hugefont = pygame.font.SysFont("Times New Roman", 160)
    largefont = pygame.font.SysFont("Times New Roman", 110)
    mediumfont = pygame.font.SysFont("Times New Roman", 85)
    smallfont = pygame.font.SysFont("Times New Roman", 40)
    textfont = pygame.font.SysFont("Times New Roman", 30)

    fonts = {}

    def __init__(self, window):
        self.buttonpadding = 20
        self.window = window

    def line(self, start, end, color, width=1):
        pygame.draw.line(self.window, color, start, end, width)

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

    def paragraph(self, text, x=20, y=20, xlim=room_width - 20):
        myfont = self.smallfont
        padding = 10
        cx = x
        cy = y
        words = text.split(" ")

        counter = 0
        while counter < len(words):
            currenttext = ""
            text_width, text_height = myfont.size(currenttext)
            while text_width < xlim - cx and counter < len(words):
                currenttext = currenttext + words[counter] + " "
                if counter < len(words) - 1:
                    text_width = myfont.size(currenttext + words[counter + 1])[0]

                counter += 1

            self.display(currenttext, cx, cy, self.colors["black"], myfont)
            cy += text_height + padding

    def create_button(self, text, x, y, font, alignment="left", crossed=False):
        global pressed

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

            if pressed:
                Text.click_sound.play()
                pressed = False
                return True

        else:
            box_colour = self.colors['white']

        pygame.draw.rect(self.window, box_colour, [box_x, box_y, box_width, box_height])
        pygame.draw.rect(self.window, self.colors['black'], [box_x, box_y, box_width, box_height], 5)
        self.display(text, text_x, text_y, self.colors['black'], font)

        if crossed:
            self.line([box_x, box_y], [box_x + box_width, box_y + box_height], Text.colors['black'], 6)
            self.line([box_x + box_width, box_y], [box_x, box_y + box_height], Text.colors['black'], 6)

    def create_border(self, x, y, width, height, thickness, colour):
        pygame.draw.rect(self.window, colour, (x, y, width, thickness))
        pygame.draw.rect(self.window, colour, (x, y, thickness, height))
        pygame.draw.rect(self.window, colour, (x + width - thickness, y, thickness, height))
        pygame.draw.rect(self.window, colour, (x, y + height - thickness, width, thickness))


class Board:
    def __init__(self, window):
        self.board = [[], [], [], [], [], [], [], []]
        self.window = window
        self.border = 5
        self.x = 100
        self.y = 100
        self.width = 600
        self.tile_width = self.width / 8

    def draw(self):
        # Draw border
        pygame.draw.rect(window, Text.colors["black"], [self.x, self.y, self.width, self.width], self.border)

        # Draw tiles
        for i in range(8):
            y = self.y + i*self.tile_width
            for j in range(8):
                x = self.x + j*self.tile_width

                if (i+j) % 2 == 0:
                    color = Text.colors["white"]
                else:
                    color = Text.colors["black"]

                pygame.draw.rect(window, color, [x, y, self.tile_width, self.tile_width])


class Piece:
    pass


def draw_background():
    window.fill(Text.bgcolor)


def draw_paused():
    text.display("P A U S E D", room_width / 2, room_height / 2, Text.colors['white'], Text.largefont, "center")


def close():
    global paused
    global stage
    global pressed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # Pause Feature
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                stage = 7

        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = True
        else:
            pressed = False


def draw():
    for obj in allobjs:
        obj.draw()


text = Text(window)
board = Board(window)


# Main Game loop
while True:
    close()
    draw_background()
    board.draw()
    if not paused:
        draw()
    else:
        draw_paused()


    pygame.time.delay(1)
    pygame.display.update()
