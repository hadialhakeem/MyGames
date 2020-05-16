import pygame
from random import randint

pygame.mixer.pre_init()
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.init()
pygame.init()

# Set up room and variables
room_width = 900
room_height = 600
window = pygame.display.set_mode((room_width, room_height))
pygame.display.set_caption("GAME_NAME")
pygame.mixer.music.load("bgm.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)

allobjs = []

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

    # Set up sound effect // Make sure you have file in directory
    click_sound = pygame.mixer.Sound("click.wav")
    click_sound.set_volume(0.25)

    fonts = {}

    def __init__(self, window):
        self.buttonpadding = 20
        self.window = window


    def line(self, start, end, color, width=1):
        pygame.draw.line(window, color, start, end, width)

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

    def paragraph(self, text, x = 20, y = 20, xlim=room_width-20):
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

    def create_button(self, text, x, y, font, alignment = "left", crossed = False):
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
    global stage
    global pressed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        #Pause Feature

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
paused = False
stage = 0
restarts = 0

# Stages
# -2 - About Me
# -1 - Help
# 0  - Main Menu
# 1  - Choose Major
# 2  - Med Sci Route
# 3  - Math route
# 4  - Math Master's
# 5  - Math Ph.D
# 6  - Microsoft route
# 7  - Google Route
# 11 - Cs major
# 12 - Cs Master

# 10 - Final Screen

# Main Game loop
while True:
    close()
    draw_background()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        stage = 0

    if stage == 0:
        text.display("My Career!", room_width/2, 0, text.colors['black'], text.largefont, 'center')

        start = text.create_button("Start!", room_width/2, 200, text.mediumfont, "center")
        help = text.create_button("Help", room_width/2, 350, text.mediumfont, "center")
        aboutme = text.create_button("About Me", room_width / 2, 500, text.mediumfont, "center")

        if start:
            stage = 1

        if help:
            stage = -1

        if aboutme:
            stage = -2

    elif stage == 1:
        text.display("Choose Your Major!", room_width/2, 0, text.colors['black'], text.largefont, 'center')

        yval = room_height/2 + 10

        math = text.create_button("Math", 150, yval + 150, text.mediumfont, "center")
        cs = text.create_button("Comp Sci", room_width/2, yval - 100, text.mediumfont, "center")

        if restarts == 0:
            med = text.create_button("Med Sci", 700, yval + 150, text.mediumfont, "center")
        else:
            med = text.create_button("Med Sci", 700, yval + 150, text.mediumfont, "center", True)


        if med and restarts == 0:
            stage = 2

        if math:
            stage = 3

        if cs:
            stage = 11


    elif stage == -1:
        text.paragraph("In this game, you will be playing as myself and choosing the career path for me to take. You can choose things such as what major I go into, and what I do after graduation. If you go down the computer science route, there is a 25% chance you will fail. If you would like to play through both possibilities, play the game again and see if you're lucky! Enjoy the game and make sure to have fun!")

        back = text.create_button("Back", room_width/2, 530, text.mediumfont, "center")

        if back:
            stage = 0

    elif stage == 2:
        text.paragraph("Hadi ends up studying Medical Science at McMaster University. He realizes he doesn't even like this subject, and isn't able to put in any effort. He fails his 1st year chemistry classes and ends up dropping out, wasting a lot of time and money. See, if you read the 'About Me' section, you would know Hadi doesn't like this subject. Reflect on your choice and restart when you're ready.")

        restart = text.create_button("Restart", room_width / 2 + 20, 530, text.mediumfont, "center")

        if restart:
            restarts += 1
            stage = 0

    elif stage == -2:
        text.paragraph("My name is Hadi, and I created this game using python. All the code is original, and can be found on my github. My main interests are math and computer science, and I would HATE to study medical science. The main path I would like is to get a degree in one of those majors, and then either work at a company or pursue research and teaching by obtaining a Ph.D and becoming a professor.")

        back = text.create_button("Back", room_width / 2, 530, text.mediumfont, "center")

        if back:
            stage = 0

    elif stage == 3:
        text.paragraph("You made a good choice! Hadi loves math and goes to the University of Waterloo to study it!! He excels in all his courses, and graduates with a Mathematics degree. He must now make a choice. Google offered Hadi a job as a Data Scientist at their company, but he also loves the subject very much and doesn't want to stop learning. Does he purse a Master's degree, or does he work as a Data Scientist? You Decide!")

        masters = text.create_button("Master's", 250, 530, text.mediumfont, "center")
        job = text.create_button("Google", 650, 530, text.mediumfont, "center")

        if masters:
            stage = 4
        if job:
            stage = 7

    elif stage == 4:
        text.paragraph("You decided that Hadi will pursue further education. He completes his Master's of Math at Waterloo, and loves the process. Luckily, Microsoft offers him a position with a high salary since he's very educated. However, through tutoring his classmates, Hadi realizes he enjoys teaching. He considers the option of becoming a Professor, which requires him to complete a Ph.D. You must now decide his next choice!")

        job = text.create_button("Microsoft", 250, 530, text.mediumfont, "center")
        phd = text.create_button("Math Ph.D", 650, 530, text.mediumfont, "center")

        if phd:
            stage = 5
        if job:
            stage = 6

    elif stage == 5:
        text.paragraph("Hadi completes his Ph.D, and becomes a teaching assistant at Waterloo, before becoming a full time Professor. He enjoys his life thoroughly. From here, he plans to continue research in math, while teaching. His dream goal is to solve one unsolved problem in mathematics, or to discover a new theorem and have it named after him. He gets married in his late 20's, and plans to have a family and be a good father.")

        next = text.create_button("Next", room_width/2, 530, text.mediumfont, "center")

        if next:
            stage = 10

    elif stage == 6:
        text.paragraph("Hadi works hard at Microsoft, and enjoys the environment along with the benefits. He gets promoted, and moves on to other jobs where he excels. He becomes a full stack developer with experience in many languages. This helps be employable at many companies.")

        next = text.create_button("Next", room_width / 2, 450, text.mediumfont, "center")

        if next:
            stage = 10

    elif stage == 7:
        text.paragraph("Hadi enjoys working at Google. He works there for many years, getting promoted before moving on to other opportunities found elsewhere. He ends up becoming a data science expert, and mainly works with large data sets, trying to find insights within the data.")

        next = text.create_button("Next", room_width / 2, 450, text.mediumfont, "center")

        if next:
            stage = 10


    elif stage == 10:
        text.paragraph("Congratulations! You completed the game. I hope you enjoyed making my decisions. Currently, I would like to go down the Math PhD/Professor route, however it is very difficult and life may take me in other directions. Play the game again and see what other options I am considering taking in my future! :)")

        playagain = text.create_button("Play Again", room_width / 2, 470, text.mediumfont, "center")

        if playagain:
            stage = 0

    elif stage == 11:
        text.paragraph("Hadi likes coding a lot, and is happy he chose to go into computer science. He goes to his first choice, the University of Waterloo. He enjoys his time there, but he also realizes he likes math just as much as computer science. Now, you must make his next decision. Should Hadi pursue a Master's in Computer science, Math, or go straight into the job market?")

        cs = text.create_button("CS", 100, 500, text.mediumfont, "center")
        math = text.create_button("Math", 310, 500, text.mediumfont, "center")
        job = text.create_button("Job Market", 650, 500, text.mediumfont, "center")

        if math:
            stage = 4

        if cs:
            stage = 12

        if job:
            stage = 13

    elif stage == 12:
        text.paragraph("Hadi obtains his master's in computer science at Waterloo. He know has 2 options to make. Google has offered Hadi a position as a software developer, with a salary of $120,000 before tax. He can take this job, or he can go into teaching as a professor which requires him to purue a PhD in comuter science. You must now make his choice!")

        phd = text.create_button("Ph.D", 250, 500, text.mediumfont, "center")
        google = text.create_button("Google", 650, 500, text.mediumfont, "center")

        if phd:
            random = randint(1, 4)
            if random == 1:
                stage = 14
            else:
                stage = 15

        if google:
            stage = 7

    elif stage == 13:
        text.paragraph("Hadi has received 2 job offers since graduating with a Bachelor's in computer science. Microsoft offers him a position at their company as a junior devoloper. Google offers him a position as a data scientist. Both positions are great options for Hadi. You must now make his decision.")

        microsoft = text.create_button("Microsoft", 250, 470, text.mediumfont, "center")
        google = text.create_button("Google", 650, 470, text.mediumfont, "center")

        if microsoft:
            stage = 6

        if google:
            stage = 7

    elif stage == 14:
        text.paragraph("Unfortunately, Hadi ends up with a poor advisor during his PhD studies. This results in him hating what he does, and dropping out of his PhD program. He must know find a job working as a software developer.")

        job = text.create_button("Find A Job", room_width/2, 470, text.mediumfont, "center")

        if job:
            stage = 16

    elif stage == 15:
        text.paragraph("Hadi finishes his PhD program and, thanks to his amazing advisor, he earns his PostDoc degree. His supervisor has connections and is able to find him a teaching job at Ryerson University. He excels there as a part time professor, before becoming full time. He goes on to teach at the University of Toronto (St. George, ofcourse) where he works full time, before becoming the Dean of Mathematics. Ultimately, Hadi is glad he went down this route.")

        next = text.create_button("Next", room_width - 220, 530, text.mediumfont, "center")

        if next:
            stage = 10

    elif stage == 16:
        text.paragraph("Luckily for Hadi, both Microsoft AND Google offer him positions at their companies. He doesn't care which company he goes to, and is simply glad that he was able to find a job so quickly! Anyways, you must choose what he does next!")

        microsoft = text.create_button("Microsoft", 250, 470, text.mediumfont, "center")
        google = text.create_button("Google", 650, 470, text.mediumfont, "center")

        if microsoft:
            stage = 6

        if google:
            stage = 7

    pygame.display.update()
