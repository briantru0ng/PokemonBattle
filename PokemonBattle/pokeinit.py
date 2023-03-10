import pygame as pg
import csv
import random
from window import *
from battle import *

movedata = []

class PokeMenu():
    def __init__(self, window):
        self.window = window
        self.width = self.window.width
        self.height= self.window.height
        self.run_display = True

        self.cursor_rect = pg.Rect(0, 0, 0, 0)
        self.offset = -120

        # open csv files for data
        stats_csv = open("Pokemon Metadata\\stats.csv", "r")
        self.stat_data = list(csv.reader(stats_csv, delimiter=","))
        stats_csv.close()

        moves_csv = open("Pokemon Metadata\\moves.csv", "r")
        self.moves_data = list(csv.reader(moves_csv, delimiter=","))
        moves_csv.close()

    def draw_cursor(self):
        self.window.insert_text(">", 25, self.cursor_rect.x, self.cursor_rect.y, (87, 81, 244))

    def blit_screen(self):
        self.window.screen.blit(self.window.display, (0, 0))
        pg.display.update()
        self.window.reset_keys()

class PokePrep(PokeMenu):
    def __init__(self, window, num_of_players):
        PokeMenu.__init__(self, window)
        print("Num Player: {}".format(num_of_players))
        self.num_of_players = num_of_players
        # set background to the image
        path="C:\\Users\\Brian\\PSU\\Z_Python Projects\\PokemonBattle\\"
        self.pokeloader = pg.image.load(path+"PokeInit.png").convert()
        # print (self.stat_data)

        dummy_offset = -20
        # the 4 pokemon available locations:
        # Torterra - to
        self.state = "T"
        self.tox, self.toy = self.width/3, self.height/4 -dummy_offset
        self.cursor_rect.midtop = (self.tox-100, self.toy+20)

        # Infernape
        self.inx, self.iny = 2*self.width/3, self.height/4-dummy_offset
        
        # Empoleon
        self.emx, self.emy = self.width/3, 3*self.height/4-dummy_offset

        # Garchomp
        self.gax, self.gay = 2*self.width/3, 3*self.height/4-dummy_offset
        
        # Moveset
        self.chosen_moves = movedata



    def display_menu(self):
        self.run_display = True
        # if self.num_of_players != 0:
        while self.run_display:
            self.window.check_events()
            self.check_menu_input()
            
            self.window.display.blit(self.pokeloader, (0, 0))
            print("Num Player: {}".format(self.num_of_players))

            # Random team generator because of the 1-Player mode
            if self.num_of_players == 0:
                print ("Only randos here")
                rand_pkmn=random.randint(1,4)
                move_index = [0, 1, 2, 3, 4, 5, 6]
                move_index = random.sample(move_index, k=4)

                potenial_moves=[]
                for row in self.moves_data:
                    if row[0] == str(rand_pkmn):
                        row.insert(0, 0)
                        potenial_moves.append(row)
                
                for index in move_index:
                    self.window.playerRandPick.chosen_moves.append(potenial_moves[index])
                    # print (self.window.playerRandPick.chosen_moves)

                
                self.window.current_menu = BattleScreen(self.window, self.window.player1Fight, self.window.playerRandFight)
                self.run_display = False
            
            else:
                # Title screen of who picks
                # which player
                requestLine="Player "+str(self.num_of_players)+"! Pick your Pokemon:"
                self.window.insert_text(requestLine, 30, self.window.width/2, self.height/6-10, self.window.black)

                # make profile cards for each pokemon
                # torterra - index 2
                self.create_profile_card(2, self.tox, self.toy)

                # infernape - index 1
                self.create_profile_card(1, self.inx, self.iny)
                
                # Empoleon - index 3
                self.create_profile_card(3, self.emx, self.emy-70)

                # Garchomp - index 4
                self.create_profile_card(4, self.gax, self.gay-70)

                # draw cursor
                self.draw_cursor()
                self.blit_screen()
                

    def create_profile_card(self, index, x, y):
        # Create background
        offset_x, offset_y = 80, 50
        card_height, card_width = 180, 165
        card = pg.Rect(x-offset_x, y-offset_y, card_width, card_height)
        pg.draw.rect(self.window.display, self.window.lightBlue, card)
        
        # load sprites
        calling_card="Sprites\\"+str(index)+"I.png"
        sprite = pg.image.load(calling_card).convert()
        self.window.display.blit(sprite, (x-offset_x+card_width/4, y-offset_y+10))

        
        for row in self.stat_data[1:]:
            if row[0] == str(index):
                name=row[1]
                # Load name
                self.window.insert_text(name, 15, x-offset_x+card_width/2, y-offset_y+100, self.window.black)
                
                # Load stats
                offset_y = 45
                stat_linept1= " HP/ATK/DEF"
                self.window.insert_text(stat_linept1, 13, x-offset_x+card_width/2, y-offset_y+115, self.window.black)

                act_statpt1= row[2]+ " " + row[3]+ " " + row[4] 
                self.window.insert_text(act_statpt1, 13, x-offset_x+card_width/2, y-offset_y+130, self.window.black)

                stat_linept2= "S.ATK/S.DEF/SPD  "
                self.window.insert_text(stat_linept2, 13, x-offset_x+card_width/2, y-offset_y+145, self.window.black)

                act_statpt2=  " " + row[5]+ " " +  " " + row[6]+ " " +  " " + row[7] + " " 
                self.window.insert_text(act_statpt2, 13, x-offset_x+card_width/2, y-offset_y+160, self.window.black)

    def check_menu_input(self):
        self.move_menu_cursor()
        if self.window.startKey:
            index = 0
            if self.state == "T":
                index = 2
            elif self.state == "I":
                index = 1
            elif self.state == "E":
                index = 3
            elif self.state == "G":
                index = 4
            
            allowable_moves = []
            for move in self.moves_data:
                if str(index) == move[0]:
                    allowable_moves.append(move)
            
            # print ("done-zo")
            # print (allowable_moves)
            moves=MovePrep(self.window, index, allowable_moves, self.num_of_players)
            self.window.current_menu = moves
            self.chosen_moves = moves.chosen_moves

            
            print (self.chosen_moves)
            self.run_display = False
            
        elif self.window.returnKey:
            self.window.current_menu = self.window.main_menu
            self.run_display = False

    def move_menu_cursor(self):
        x_offset = -100
        y_offset = 20
        if self.window.dKey:
            if self.state == "T":
                self.state = "E"
                self.cursor_rect.midtop = (self.emx + x_offset, self.emy - 3* y_offset)
            
            elif self.state == "E":
                self.state = "T"
                self.cursor_rect.midtop = (self.tox + x_offset, self.toy + y_offset)
                
            elif self.state == "I":
                self.state = "G"
                self.cursor_rect.midtop = (self.gax + x_offset, self.gay - 3*y_offset)
                
            elif self.state == "G":
                self.state = "I"
                self.cursor_rect.midtop = (self.inx + x_offset, self.iny + y_offset)
        
        # Right Key
        elif self.window.rKey:
            if self.state == "T":
                self.state = "I"
                self.cursor_rect.midtop = (self.inx + x_offset, self.iny + y_offset)
            
            elif self.state == "I":
                self.state = "T"
                self.cursor_rect.midtop = (self.tox + x_offset, self.toy + y_offset)

            elif self.state == "E":
                self.state = "G"
                self.cursor_rect.midtop = (self.gax + x_offset, self.gay - 3* y_offset)

            elif self.state == "G":
                self.state = "E"
                self.cursor_rect.midtop = (self.emx + x_offset, self.emy - 3* y_offset)

        # Left Key
        elif self.window.lKey:
            if self.state == "T":
                self.state = "I"
                self.cursor_rect.midtop = (self.inx + x_offset, self.iny + y_offset)
            
            elif self.state == "I":
                self.state = "T"
                self.cursor_rect.midtop = (self.tox + x_offset, self.toy + y_offset)

            elif self.state == "E":
                self.state = "G"
                self.cursor_rect.midtop = (self.gax + x_offset, self.gay - 3* y_offset)

            elif self.state == "G":
                self.state = "E"
                self.cursor_rect.midtop = (self.emx + x_offset, self.emy - 3* y_offset)

        # Up Key
        elif self.window.uKey:
            if self.state == "T":
                self.state = "E"
                self.cursor_rect.midtop = (self.emx + x_offset, self.emy - 3*y_offset)
            
            elif self.state == "E":
                self.state = "T"
                self.cursor_rect.midtop = (self.tox + x_offset, self.toy + y_offset)
                
            elif self.state == "I":
                self.state = "G"
                self.cursor_rect.midtop = (self.gax + x_offset, self.gay - 3* y_offset)
                
            elif self.state == "G":
                self.state = "I"
                self.cursor_rect.midtop = (self.inx + x_offset, self.iny + y_offset)

class MovePrep(PokeMenu):
    def __init__(self, window, pokeIndex, moves, player_num):
        PokeMenu.__init__(self, window)
        self.pokeIndex = pokeIndex

        # set background to the image
        path="C:\\Users\\Brian\\PSU\\Z_Python Projects\\PokemonBattle\\"
        self.pokeloader = pg.image.load(path+"PokeInit.png").convert()
        
        # two lists of chosen moves and moves you can choose
        self.moves = moves
        self.chosen_moves = []

        self.state = 1
        self.player_num = player_num

        self.top_move_x, self.top_move_y = 150, 150
        self.cursor_rect.midtop = (self.top_move_x-35, self.top_move_y+20)
        self.cursor_x, self.cursor_y = self.top_move_x-35, self.top_move_y+20

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.window.check_events()
            self.check_menu_input()
            
            self.window.display.blit(self.pokeloader, (0, 0))
            # Title screen of the choose your moves
            requestLine="Pick your Pokemon's Moves"
            self.window.insert_text(requestLine, 30, self.window.width/2, self.height/6-10, self.window.black)
            self.window.insert_text("Choose up to 4 Moves", 20, self.window.width/2, self.height/6+20, self.window.black)

            self.create_move_list()


            confimation="I'm good with my moves!"
            self.window.insert_text(confimation, 20, 3*self.window.width/4, 5*self.height/6+40, self.window.black)

            self.draw_cursor()
            self.blit_screen()

    def create_move_list(self):
        tag_width, tag_height = 550, 40
        counter = 0
        for row in self.moves:
            # print (row)
            tag = pg.Rect(self.top_move_x - 25, self.top_move_y + counter*(tag_height+10),tag_width, tag_height)
            move_info1= row[1]+" | Type: "+row[2]+" | Style: "+row[3]
            move_info2="Power: "+row[4]+" | Accuracy: "+row[5]+" | Uses: "+row[6]
            move_info=(move_info1, move_info2)
            self.draw_tag(tag, row[2], move_info, (self.width/2, 10+self.top_move_y + counter*(tag_height+10)))
            counter += 1

    def draw_tag(self, tag, type, move_info, text_placement):
        # get colored tags based on the type

        grassC = (100, 238, 123) # black text
        fireC = (253, 49, 49)
        waterC = (140, 167, 255)
        groundC = (182, 168, 78)
        dragonC = (120, 78, 182)
        iceC = (140, 239, 255) # black text
        poisonC = (160, 108, 238)
        normalC = (255, 255, 204) # black text
        darkC = (57, 57, 57)
        flyingC = (214, 250, 255) # black text
        steelC = (144, 144, 144)
        rockC = (146, 125, 75)
        fightC = (215, 94, 2)
        font_size = 17

        if type == "Grass":
            pg.draw.rect(self.window.display, grassC, tag)
            self.window.insert_text(move_info[0], font_size, text_placement[0], text_placement[1], self.window.black)
            self.window.insert_text(move_info[1], font_size, text_placement[0], text_placement[1]+20, self.window.black)

        elif type == "Fire":
            pg.draw.rect(self.window.display, fireC, tag)
            self.window.insert_text(move_info[0], font_size, text_placement[0], text_placement[1], self.window.white)
            self.window.insert_text(move_info[1], font_size, text_placement[0], text_placement[1]+20, self.window.white)


        elif type == "Water":
            pg.draw.rect(self.window.display, waterC, tag)
            self.window.insert_text(move_info[0], font_size, text_placement[0], text_placement[1], self.window.white)
            self.window.insert_text(move_info[1], font_size, text_placement[0], text_placement[1]+20, self.window.white)


        elif type == "Ground":
            pg.draw.rect(self.window.display, groundC, tag)
            self.window.insert_text(move_info[0], font_size, text_placement[0], text_placement[1], self.window.white)
            self.window.insert_text(move_info[1], font_size, text_placement[0], text_placement[1]+20, self.window.white)


        elif type == "Dragon":
            pg.draw.rect(self.window.display, dragonC, tag)
            self.window.insert_text(move_info[0], font_size, text_placement[0], text_placement[1], self.window.white)
            self.window.insert_text(move_info[1], font_size, text_placement[0], text_placement[1]+20, self.window.white)


        elif type == "Ice":
            pg.draw.rect(self.window.display, iceC, tag)
            self.window.insert_text(move_info[0], font_size, text_placement[0], text_placement[1], self.window.black)
            self.window.insert_text(move_info[1], font_size, text_placement[0], text_placement[1]+20, self.window.black)


        elif type == "Poison":
            pg.draw.rect(self.window.display, poisonC, tag)
            self.window.insert_text(move_info[0], font_size, text_placement[0], text_placement[1], self.window.white)
            self.window.insert_text(move_info[1], font_size, text_placement[0], text_placement[1]+20, self.window.white)


        elif type == "Normal":
            pg.draw.rect(self.window.display, normalC, tag)
            self.window.insert_text(move_info[0], font_size, text_placement[0], text_placement[1], self.window.black)
            self.window.insert_text(move_info[1], font_size, text_placement[0], text_placement[1]+20, self.window.black)


        elif type == "Dark":
            pg.draw.rect(self.window.display, darkC, tag)
            self.window.insert_text(move_info[0], font_size, text_placement[0], text_placement[1], self.window.white)
            self.window.insert_text(move_info[1], font_size, text_placement[0], text_placement[1]+20, self.window.white)


        elif type == "Flying":
            pg.draw.rect(self.window.display, flyingC, tag)
            self.window.insert_text(move_info[0], font_size, text_placement[0], text_placement[1], self.window.black)
            self.window.insert_text(move_info[1], font_size, text_placement[0], text_placement[1]+20, self.window.black)


        elif type == "Steel":
            pg.draw.rect(self.window.display, steelC, tag)
            self.window.insert_text(move_info[0], font_size, text_placement[0], text_placement[1], self.window.white)
            self.window.insert_text(move_info[1], font_size, text_placement[0], text_placement[1]+20, self.window.white)

        elif type == "Rock":
            pg.draw.rect(self.window.display, rockC, tag)
            self.window.insert_text(move_info[0], font_size, text_placement[0], text_placement[1], self.window.white)
            self.window.insert_text(move_info[1], font_size, text_placement[0], text_placement[1]+20, self.window.white)
        
        elif type == "Fighting":
            pg.draw.rect(self.window.display, fightC, tag)
            self.window.insert_text(move_info[0], font_size, text_placement[0], text_placement[1], self.window.white)
            self.window.insert_text(move_info[1], font_size, text_placement[0], text_placement[1]+20, self.window.white)

    def check_menu_input(self):
        self.move_menu_cursor()
        self.max_state = len(self.moves)+1
        if self.window.startKey:
            # print (self.state)

            if len(self.chosen_moves) == 0 and self.state == self.max_state:
                self.window.insert_text("'You can't have a Pokemon with no moves! That's so useless!!'", 17, self.window.width/2, 5*self.height/6+10, self.window.black)
                self.blit_screen()
                pg.time.delay(2500)
                # print ("bruh")

            elif len(self.chosen_moves) <= 3:
                if self.state == self.max_state:
                    if self.window.main_menu.state == "1-Player" and self.window.playerRandPick.chosen_moves == []:
                        self.window.player1Pick.chosen_moves = self.chosen_moves
                        
                        self.window.current_menu = self.window.playerRandPick

                    elif self.window.main_menu.state == "2-Player" and self.window.player2Pick.chosen_moves == []:
                        self.window.current_menu = self.window.player2Pick

                    else:
                        print("battle ready!")
                        self.window.current_menu = BattleScreen(self.window, self.window.player1Fight, self.window.player2Fight)

                elif self.state == 1:
                    row = self.moves[self.state-1].copy()
                    row.insert(0,self.player_num)
                    self.chosen_moves.append(row)
                    self.moves.remove(self.moves[self.state-1])
                
                elif self.state == 2:
                    row = self.moves[self.state-1].copy()
                    row.insert(0,self.player_num)
                    self.chosen_moves.append(row)
                    self.moves.remove(self.moves[self.state-1])
                
                elif self.state == 3:
                    row = self.moves[self.state-1].copy()
                    row.insert(0,self.player_num)
                    self.chosen_moves.append(row)
                    self.moves.remove(self.moves[self.state-1])
                
                elif self.state == 4:
                    row = self.moves[self.state-1].copy()
                    row.insert(0,self.player_num)
                    self.chosen_moves.append(row)
                    self.moves.remove(self.moves[self.state-1])
                
                elif self.state == 5:
                    row = self.moves[self.state-1].copy()
                    row.insert(0,self.player_num)
                    self.chosen_moves.append(row)
                    self.moves.remove(self.moves[self.state-1])
                
                elif self.state == 6:
                    row = self.moves[self.state-1].copy()
                    row.insert(0,self.player_num)
                    self.chosen_moves.append(row)
                    self.moves.remove(self.moves[self.state-1])
                
                elif self.state == 7:
                    row = self.moves[self.state-1].copy()
                    row.insert(0,self.player_num)
                    self.chosen_moves.append(row)
                    self.moves.remove(self.moves[self.state-1])
                
                # PokePrep.chosen_moves = self.chosen_moves
                # print(PokePrep.chosen_moves)
                # print ((self.chosen_moves))
            elif len(self.chosen_moves) == 4 and self.state == self.max_state:      
                if self.window.main_menu.state == "1-Player" and self.window.playerRandPick.chosen_moves == []:
                    self.window.player1Pick.chosen_moves = self.chosen_moves
                    self.window.current_menu = self.window.playerRandPick

                elif self.window.main_menu.state == "2-Player" and self.window.player2Pick.chosen_moves == []:
                    self.window.current_menu = self.window.player2Pick

                else:
                    print("battle ready!")
                    self.window.current_menu = BattleScreen(self.window, self.window.player1Fight, self.window.player2Fight)
            
            
            self.run_display = False
            
        elif self.window.returnKey:
            if self.chosen_moves == []:
                self.window.current_menu = self.window.player1Pick

            else:
                # print ("return")

                # print(self.chosen_moves[-1])
                # print(self.chosen_moves[-1][1:])
                self.moves.append(self.chosen_moves[-1][1:])
                self.chosen_moves=self.chosen_moves[:-1]
                self.max_state += 1
                if self.state +1 == self.max_state:
                    self.state += 1
            self.run_display = False

    def move_menu_cursor(self):
        # Down Key
        if self.window.dKey:
            if self.state == self.max_state:
                self.state = 1
                self.cursor_x, self.cursor_y = self.top_move_x-35, self.top_move_y+20
                self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)

            elif self.state == 1:
                self.state += 1
                self.cursor_y+=self.top_move_y/3
                                
                if self.state == self.max_state:
                    self.cursor_rect.midtop = (3*self.window.width/4-170, 5*self.height/6+40)
                else:
                    self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)
            
            elif self.state == 2:
                self.state += 1
                self.cursor_y+=self.top_move_y/3
                                
                if self.state == self.max_state:
                    self.cursor_rect.midtop = (3*self.window.width/4-170, 5*self.height/6+40)
                else:
                    self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)
             
            elif self.state == 3:
                self.state += 1
                self.cursor_y+=self.top_move_y/3
                                
                if self.state == self.max_state:
                    self.cursor_rect.midtop = (3*self.window.width/4-170, 5*self.height/6+40)
                else:
                    self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)
             
            elif self.state == 4:
                self.state += 1
                self.cursor_y+=self.top_move_y/3
                                
                if self.state == self.max_state:
                    self.cursor_rect.midtop = (3*self.window.width/4-170, 5*self.height/6+40)
                else:
                    self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)
             
            elif self.state == 5:
                self.state += 1
                self.cursor_y+=self.top_move_y/3
                                
                if self.state == self.max_state:
                    self.cursor_rect.midtop = (3*self.window.width/4-170, 5*self.height/6+40)
                else:
                    self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)
             
            elif self.state == 6:
                self.state += 1
                self.cursor_y+=self.top_move_y/3

                if self.state == self.max_state:
                    self.cursor_rect.midtop = (3*self.window.width/4-170, 5*self.height/6+40)
                else:
                    self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)
             
            elif self.state == 7:
                self.state += 1
                self.cursor_y+=self.top_move_y/3   

                if self.state == self.max_state:
                    self.cursor_rect.midtop = (3*self.window.width/4-170, 5*self.height/6+40)
                else:
                    self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)
               
        # Up Key
        elif self.window.uKey:
            if self.state == self.max_state:
                self.state = self.max_state-1
                self.cursor_x, self.cursor_y = (self.top_move_x)-35, ((self.max_state-2)*self.top_move_y/3)+self.top_move_y+20
                self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)

            elif self.state == 1:
                self.state = self.max_state
                self.cursor_y-=self.top_move_y/3
                                
                if self.state == self.max_state:
                    self.cursor_rect.midtop = (3*self.window.width/4-170, 5*self.height/6+40)
                else:
                    self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)
            
            elif self.state == 2:
                self.state -= 1
                self.cursor_y-=self.top_move_y/3
                                
                if self.state == self.max_state:
                    self.cursor_rect.midtop = (3*self.window.width/4-170, 5*self.height/6+40)
                else:
                    self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)
             
            elif self.state == 3:
                self.state -= 1
                self.cursor_y-=self.top_move_y/3
                                
                if self.state == self.max_state:
                    self.cursor_rect.midtop = (3*self.window.width/4-170, 5*self.height/6+40)
                else:
                    self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)
             
            elif self.state == 4:
                self.state -= 1
                self.cursor_y-=self.top_move_y/3
                                
                if self.state == self.max_state:
                    self.cursor_rect.midtop = (3*self.window.width/4-170, 5*self.height/6+40)
                else:
                    self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)
             
            elif self.state == 5:
                self.state -= 1
                self.cursor_y-=self.top_move_y/3
                                
                if self.state == self.max_state:
                    self.cursor_rect.midtop = (3*self.window.width/4-170, 5*self.height/6+40)
                else:
                    self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)
             
            elif self.state == 6:
                self.state -= 1
                self.cursor_y-=self.top_move_y/3

                if self.state == self.max_state:
                    self.cursor_rect.midtop = (3*self.window.width/4-170, 5*self.height/6+40)
                else:
                    self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)
             
            elif self.state == 7:
                self.state -= 1
                self.cursor_y-=self.top_move_y/3   

                if self.state == self.max_state:
                    self.cursor_rect.midtop = (3*self.window.width/4-170, 5*self.height/6+40)
                else:
                    self.cursor_rect.midtop = (self.cursor_x, self.cursor_y)

