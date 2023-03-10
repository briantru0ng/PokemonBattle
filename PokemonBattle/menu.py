import pygame as pg
from window import *

class Menu():
    def __init__(self, window):
        self.window = window
        self.mid_width = self.window.width/2
        self.lower_height= 3*self.window.height/4
        self.run_display = True

        self.cursor_rect = pg.Rect(0, 0, 20, 20)
        self.offset = -120

    def draw_cursor(self):
        self.window.insert_text(">", 25, self.cursor_rect.x, self.cursor_rect.y, (87, 81, 244))

    def blit_screen(self):
        self.window.screen.blit(self.window.display, (0, 0))
        pg.display.update()
        self.window.reset_keys()


class MainMenu(Menu):
    def __init__(self, window):
        Menu.__init__(self, window)
        # set backkground to the image
        path="C:\\Users\\Brian\\PSU\\Z_Python Projects\\PokemonBattle\\"
        self.titlepic = pg.image.load(path+"TitleCard.png").convert()
        
        
        # create text labels for main menu
        # Start Text
        self.startx, self.starty = self.mid_width, self.lower_height-30
        
        # Assume program starts at choice 1-Player and create a label for it
        self.state = "1-Player"
        self.opx, self.opy = self.mid_width+2*self.offset/3, self.lower_height
        self.cursor_rect.midtop = (self.opx - 60, self.opy)

        # 2-Player
        self.tpx, self.tpy = self.mid_width-2*self.offset/3, self.lower_height

        # About This Project
        self.atpx, self.atpy = self.mid_width, self.lower_height+ 30

        # Credit
        self.credx, self.credy = self.mid_width, self.lower_height+ 60

        # Exit
        self.exitx, self.exity = self.mid_width, self.lower_height+ 90

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.window.check_events()
            self.check_menu_input()
            
            self.window.display.blit(self.titlepic, (0, 0))
            

            # Title Card
            self.window.insert_text("Pokemon Battle Simulator", 40, self.window.width/2, self.window.height/2-100, self.window.black)

            #
            self.window.insert_text("A 1 vs. 1 Battle to see who is the best trainer! ", 20, self.window.width/2, self.window.height/2-55, self.window.black)

            subfont_size = 30
            # Start
            self.window.insert_text("Start Game", subfont_size, self.startx, self.starty, self.window.white)  
            
            # 1-Player
            self.window.insert_text("1-Player", subfont_size-10, self.opx, self.opy, self.window.white)  
            
            # 2-Player
            self.window.insert_text("2-Player", subfont_size-10, self.tpx, self.tpy, self.window.white)  
            
            # About This Project
            self.window.insert_text("About this project", subfont_size, self.atpx, self.atpy, self.window.white)    
            
            # Credit
            self.window.insert_text("Credit", subfont_size, self.credx, self.credy, self.window.white)  
            
            # Exit
            self.window.insert_text("Exit", subfont_size, self.exitx, self.exity, self.window.white)


            # draw cursor
            self.draw_cursor()
            self.blit_screen()

    def move_menu_cursor(self):
        atp_offset = 100
        p_offset = 60
        
        # Down Key
        if self.window.dKey:
            if self.state == "1-Player":
                self.state = "ATP"
                self.cursor_rect.midtop = (self.atpx + self.offset - atp_offset, self.atpy)

            elif self.state == "2-Player":
                self.state = "ATP"
                self.cursor_rect.midtop = (self.atpx + self.offset - atp_offset, self.atpy)

            elif self.state == "ATP":
                self.state = "Credit"
                self.cursor_rect.midtop = (self.credx + self.offset, self.credy)

            elif self.state == "Credit":
                self.state = "Exit"
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)

            elif self.state == "Exit":
                self.state = "1-Player"
                self.cursor_rect.midtop = (self.opx - p_offset, self.opy)
        
        # Right Key
        elif self.window.rKey:
            if self.state == "1-Player":
                self.state = "2-Player"
                self.cursor_rect.midtop = (self.tpx - p_offset, self.tpy)
            
            elif self.state == "2-Player":
                self.state = "1-Player"
                self.cursor_rect.midtop = (self.opx - p_offset, self.opy)
        
        # Left Key
        elif self.window.lKey:
            if self.state == "2-Player":
                self.state = "1-Player"
                self.cursor_rect.midtop = (self.opx - p_offset, self.opy)

            elif self.state == "1-Player":
                self.state = "2-Player"
                self.cursor_rect.midtop = (self.tpx - p_offset, self.tpy)

        # Up Key
        elif self.window.uKey:
            if self.state == "1-Player":
                self.state = "Exit"
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)

            elif self.state == "2-Player":
                self.state = "Exit"
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)

            elif self.state == "ATP":
                self.state = "1-Player"
                self.cursor_rect.midtop = (self.opx - p_offset, self.opy)

            elif self.state == "Credit":
                self.state = "ATP"
                self.cursor_rect.midtop = (self.atpx + self.offset - atp_offset, self.atpy)

            elif self.state == "Exit":
                self.state = "Credit"
                self.cursor_rect.midtop = (self.credx + self.offset, self.credy)

    def check_menu_input(self):
        '''
        changes screens based on the state it is in when a 'enter' key is pressed
        '''
        self.move_menu_cursor()
        if self.window.startKey:
            # print (self.state)
            if self.state == "1-Player" or self.state == "2-Player":
                self.window.battle = True
                self.window.current_menu = self.window.player1Pick
            elif self.state == "ATP":
                self.window.current_menu = self.window.atp_menu
            elif self.state == "Credit":
                self.window.current_menu = self.window.credit_menu
            elif self.state == "Exit":
                self.window.startup = False
                self.window.battle = False
            
            self.run_display = False

class AboutTheProject(Menu):
    def __init__(self, window):
        Menu.__init__(self, window)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.window.check_events()
            if self.window.returnKey:
                self.window.current_menu = self.window.main_menu
                self.run_display = False
            
            self.window.display.fill(self.window.darkBlue)
            
            # Message
            self.window.insert_text("Hello Hello!", 30, self.window.width/2, self.window.height/6, self.window.white)
            text_size= 17
            self.window.insert_text("This project was made recently to show off my python",         text_size, self.window.width/2, self.window.height/3, self.window.white)
            self.window.insert_text("function and classes. I made a similar game like this",       text_size, self.window.width/2, self.window.height/3+1*text_size, self.window.white)
            self.window.insert_text("before in my freshamn year of High School, but I never ",      text_size, self.window.width/2, self.window.height/3+2*text_size, self.window.white)
            self.window.insert_text("got around to reworking on it (well it was written in ",            text_size, self.window.width/2, self.window.height/3+3*text_size, self.window.white)
            self.window.insert_text("QBasic and it was in 1 file). Redoing this to see how", text_size, self.window.width/2, self.window.height/3+4*text_size, self.window.white) 
            self.window.insert_text("far I've come since then.", text_size, self.window.width/2, self.window.height/3+5*text_size, self.window.white)
            text_size= 20
            self.window.insert_text("As far as instructions go,",                           text_size, self.window.width/2, self.window.height/3+6*text_size, self.window.white)
            self.window.insert_text("Use the arrow keys for moving the cursor",             text_size, self.window.width/2, self.window.height/3+7*text_size, self.window.white)
            self.window.insert_text("The backspace button to return to the previous page",  text_size, self.window.width/2, self.window.height/3+8*text_size, self.window.white)
            self.window.insert_text("The enter button to confirm a choice",                 text_size, self.window.width/2, self.window.height/3+9*text_size, self.window.white)

            self.blit_screen()

class Credit(Menu):
    def __init__(self, window):
        Menu.__init__(self, window)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.window.check_events()
            if self.window.returnKey:
                self.window.current_menu = self.window.main_menu
                self.run_display = False
            
            self.window.display.fill(self.window.darkBlue)
            
            # Message
            self.window.insert_text("Made by me!", 30, self.window.width/2, self.window.height/2, self.window.white)
            self.window.insert_text("Brian Truong", 30, self.window.width/2, self.window.height/2 + 30, self.window.white)

            self.blit_screen()

class RandomWin(Menu):
    def __init__(self, window):
        Menu.__init__(self, window)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.window.check_events()
            if self.window.returnKey:
                self.window.current_menu = self.window.main_menu
                self.run_display = False
            
            self.window.display.fill(self.window.darkBlue)
            
            # Message
            self.window.insert_text("You Lost Player 1", 30, self.window.width/2, self.window.height/2, self.window.white)
            self.window.insert_text("Good luck next time", 30, self.window.width/2, self.window.height/2 + 30, self.window.white)

            self.blit_screen()

class P1Win(Menu):
    def __init__(self, window):
        Menu.__init__(self, window)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.window.check_events()
            if self.window.returnKey:
                self.window.current_menu = self.window.main_menu
                self.run_display = False
            
            self.window.display.fill(self.window.darkBlue)
            
            # Message
            self.window.insert_text("Player 1 Wins!!", 30, self.window.width/2, self.window.height/2, self.window.white)
            self.window.insert_text("Congratulations", 30, self.window.width/2, self.window.height/2 + 30, self.window.white)

            self.blit_screen()

class P2Win(Menu):
    def __init__(self, window):
        Menu.__init__(self, window)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.window.check_events()
            if self.window.returnKey:
                self.window.current_menu = self.window.main_menu
                self.run_display = False
            
            self.window.display.fill(self.window.darkBlue)
            
            # Message
            self.window.insert_text("Player 2 Wins!!", 30, self.window.width/2, self.window.height/2, self.window.white)
            self.window.insert_text("Congratulations", 30, self.window.width/2, self.window.height/2 + 30, self.window.white)

            self.blit_screen()
    
