import pygame as pg
from pygame.locals import *
from menu import *
from pokeinit import *
from battle import *
import csv



class Window():
    def __init__(self):
        # important initializations
        pg.init()

        self.startup = True
        self.battle = False
        self.width = 800
        self.height = 600
        self.display = pg.Surface((self.width, self.height))
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Pokemon Battle!")
        self.font = 'Monocraft.otf'

        # Screens
        self.main_menu = MainMenu(self)
        self.atp_menu = AboutTheProject(self)
        self.credit_menu = Credit(self) 

        self.player1Pick = PokePrep(self, 1)
        self.player2Pick = PokePrep(self, 2)
        self.playerRandPick = PokePrep(self, 0)

        self.player1win_menu = P1Win(self)
        self.player2win_menu = P2Win(self)
        self.randomwin_menu = RandomWin(self)

        self.current_menu = self.main_menu

        # Player data
        self.player1Fight = Pokemon([0, 0, 0, 0, 0, 0, 0, 0],[[0]])
        self.player2Fight = Pokemon([0, 0, 0, 0, 0, 0, 0, 0],[[0]])
        self.playerRandFight = Pokemon([0, 0, 0, 0, 0, 0, 0, 0],[[0]])
    

        # movement keys
        self.uKey = False
        self.rKey = False
        self.lKey = False
        self.dKey = False

        # confirm keys
        self.startKey = False
        self.returnKey = False

        # colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.darkBlue = (17, 17, 76)
        self.lightBlue = (130, 192, 255)
    
    def game_loop(self):
        while self.battle:
            self.check_events()
            if self.startKey:
                self.battle = False

            #reset the screen to black
            self.display.fill (self.black)            

            
            if (self.main_menu.state == "2-Player"):
                self.write_to_csv(self.player1Pick.chosen_moves, self.player2Pick.chosen_moves)

                return 
            elif (self.main_menu.state == "1-Player"):
                self.player2Pick.chosen_moves=[]
                self.write_to_csv(self.player1Pick.chosen_moves, self.playerRandPick.chosen_moves)

                return 


            self.screen.blit(self.display, (0, 0))
            pg.display.update()
            self.reset_keys()
            
            


    def check_events(self):
        for event in pg.event.get():
            # exit the program entirely
            if event.type == pg.QUIT:
                with open('Pokemon Metadata\\curr_hp.csv', 'w', newline='') as file1:
                    writera = csv.writer(file1)
                    # writera.writerow([])
                file1.close()    
                self.startup = False
                self.battle = False
                self.current_menu.run_display = False
            
            if event.type == pg.KEYDOWN:
                # movement keys
                if event.key == pg.K_UP:
                    self.uKey = True
                              
                elif event.key == pg.K_RIGHT:
                    self.rKey = True
                   
                elif event.key == pg.K_LEFT:
                    self.lKey = True
                  
                elif event.key == pg.K_DOWN:
                    self.dKey = True
                
                # confirm key
                elif event.key == pg.K_RETURN:
                    self.startKey = True
                    
                elif event.key == pg.K_BACKSPACE:
                    if self.current_menu == self.main_menu:
                        self.startup = False
                        self.battle = False
                        self.current_menu.run_display = False
                    self.returnKey = True
                        
    def reset_keys(self):
        # movement keys
        self.uKey = False
        self.rKey = False
        self.lKey = False
        self.dKey = False

        # confirm keys
        self.startKey = False
        self.returnKey = False
    
    def insert_text(self, text, size, x, y, color):
        '''
        Creates a text box of given string 'text' of size 'size' in the positioning of (x,y)
        '''

        font = pg.font.Font(self.font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center= (x,y)

        self.display.blit(text_surface, text_rect)

    def write_to_csv(self, moveset1, moveset2):
        # print ("time to write")
        with open("Pokemon Metadata\\movesets.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            for move in moveset1:
                writer.writerow(move)

            for move in moveset2:
                writer.writerow(move)
