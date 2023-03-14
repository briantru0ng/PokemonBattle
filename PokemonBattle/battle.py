import pygame as pg
import csv
import random
from pokeinit import *
from window import *

class Pokemon():
    def __init__(self, stats, moves):
        self.moves = moves
        self.random = moves[-1][0] # 0 if random
        self.index = stats[0]
        self.typing = []
        if self.index == '1':
            self.typing = [["Fire"], ["Fighting"]]
        elif self.index == '2':
            self.typing = [["Grass"], ["Ground"]]
        elif self.index == '3':
            self.typing = [["Water"], ["Steel"]]
        else:
            self.typing = [["Dragon"], ["Ground"]]
        self.name = stats[1]
        self.max_hp=int(stats[2])
        self.current_hp = int(stats[2])
        self.atk = int(stats[3])
        self.defense = int(stats[4])
        self.satk = int(stats[5])
        self.sdef = int(stats[6])
        self.spd = int(stats[7])
        
        

class BattleMenu():
    def __init__(self, window):
        self.window = window
        self.width = self.window.width
        self.height= self.window.height
        self.run_display = True

        self.cursor_rect = pg.Rect(0, 0, 0, 0)

        # open csv files for data
        stats_csv = open("Pokemon Metadata\\stats.csv", "r")
        self.stat_data = list(csv.reader(stats_csv, delimiter=","))
        stats_csv.close()

        moveset_csv = open("Pokemon Metadata\\movesets.csv", "r")
        self.moveset_data = list(csv.reader(moveset_csv, delimiter=","))
        moveset_csv.close()

    def draw_cursor(self):
        self.window.insert_text(">", 25, self.cursor_rect.x, self.cursor_rect.y, (255, 255, 255))

    def blit_screen(self):
        self.window.screen.blit(self.window.display, (0, 0))
        pg.display.update()
        self.window.reset_keys()

class BattleScreen(BattleMenu):
    '''
    Battle sequence b/w 2 players and solo-play and handler of events based on selected moves
    '''
    def __init__(self, window, p1, p2):
        BattleMenu.__init__(self, window)
        self.p1 = p1
        self.p2 = p2

        self.phase = 1
        self.path="C:\\Users\\Brian\\PSU\\Z_Python Projects\\PokemonBattle\\"
        self.pokeloader = pg.image.load(self.path+"Battlelayout.png").convert()

        self.tlx = self.width/20
        self.tly = 550
        self.cursor_rect.midtop = (self.tlx, self.tly)
        self.state = 1
        self.max_state = 1
        self.phase = 1
        self.attacking_move= {1:[], 2:[]}

    def display_menu(self):
        '''
        loop that checks for the potenital comfirmation of moves
        '''
        self.run_display = True
        while self.run_display:
            self.window.check_events()
            self.check_menu_input()
            self.window.display.blit(self.pokeloader, (0, 0))

            self.p1, self.p2 = self.csv_splitter()
            
            if self.phase == 1:
                # player1 chooses a move
                self.display_pokemon(self.p1.index, self.p2.index) # displays in favor of p1
                self.display_pokemon_info(self.p1, self.p2, 0)
                self.max_state = len(self.p1.moves)
                self.window.insert_text("What will you do Player 1?", 25, self.width/2, 465,self.window.black)

                self.choose_move(self.p1.moves)

            elif self.phase == 2:
                self.display_pokemon(self.p2.index, self.p1.index) # displays in favor of p2
                self.display_pokemon_info(self.p2, self.p1, 1)
                self.window.insert_text("What will you do Player 2?", 25, self.width/2, 465,self.window.black)

                self.max_state = len(self.p2.moves)
                self.choose_move(self.p2.moves)
   
            if self.attacking_move[1] != [] and self.attacking_move[2] != []:
                print ("time to ATTACKKKKK!!")
                pg.time.delay(1000)
                if self.p1.spd >= self.p2.spd:
                    print("done")
                    

                else:
                    print ("slower")
                self.p1.current_hp -= 20

                curr_hp_data = open("Pokemon Metadata\\curr_hp.csv", "r")
                curr_hp = list(csv.reader(curr_hp_data, delimiter=","))
                curr_hp_data.close()
                print("main way", curr_hp)
                rand_dmg_1 = random.randint(20, 100)
                rand_dmg_2 = random.randint(20, 100)

                calc_dmg_on_p1 = self.calculatedDMG(self.attacking_move[2], self.p2, self.p1)
                calc_dmg_on_p2 = self.calculatedDMG(self.attacking_move[1], self.p1, self.p2)


                print("P1 new way:", [int(curr_hp[0][0])-20])
                rowb= [[int(curr_hp[0][0])-calc_dmg_on_p1],[int(curr_hp[1][0])-calc_dmg_on_p2]]
                with open('Pokemon Metadata\\curr_hp.csv', 'w', newline='') as file1:
                    writera = csv.writer(file1)
                    print("rows: ", rowb)
                    writera.writerow(rowb[0])
                    writera.writerow(rowb[1])

                file1.close()    
                
                print (self.p2.random)
                self.attacking_move[1]=[]
                self.attacking_move[2]=[]

                if rowb[0][0] <= 0:
                    print ("player two wins")
                    with open('Pokemon Metadata\\curr_hp.csv', 'w', newline='') as file1:
                        writera = csv.writer(file1)
                        # writera.writerow([])
                    file1.close()   
                    if self.p2.random == '0':
                        self.window.current_menu = self.window.randomwin_menu
                    else:
                        self.window.current_menu = self.window.player2win_menu
                        

                elif rowb[1][0] <= 0:
                    print ("player one wins")
                    with open('Pokemon Metadata\\curr_hp.csv', 'w', newline='') as file1:
                        writera = csv.writer(file1)
                        # writera.writerow([])
                    file1.close()   
                    self.window.current_menu = self.window.player1win_menu


            self.draw_cursor()
            self.blit_screen()

    def csv_splitter(self):
        '''
        Rips from the csv files in the metadata folder and makes Pokemon Classes based on the pokemon picked in the picking stage
        '''
        stats_csv = open("Pokemon Metadata\\stats.csv", "r")
        stat_data = list(csv.reader(stats_csv, delimiter=","))
        stats_csv.close()

        moveset_csv = open("Pokemon Metadata\\movesets.csv", "r")
        moveset_data = list(csv.reader(moveset_csv, delimiter=","))
        moveset_csv.close()

        player1Move = []
        player2Move = []

        for move in moveset_data:
            if move[0] == '1':
                player1Move.append(move[1:])
            else:
                player2Move.append(move[1:])
                reality = move[0]

        player1Index = player1Move[0][0]
        player2Index = player2Move[0][0]

        if player1Index == "1":
            pokemon_of_p1 = Pokemon(stat_data[1], player1Move)

        elif player1Index == "2":
            pokemon_of_p1 = Pokemon(stat_data[2], player1Move)

        elif player1Index == "3":
            pokemon_of_p1 = Pokemon(stat_data[3], player1Move)

        elif player1Index == "4":
            pokemon_of_p1 = Pokemon(stat_data[4], player1Move)


        if player2Index == "1":
            pokemon_of_p2 = Pokemon(stat_data[1], player2Move)
            pokemon_of_p2.random = reality
        elif player2Index == "2":
            pokemon_of_p2 = Pokemon(stat_data[2], player2Move)
            pokemon_of_p2.random = reality

        elif player2Index == "3":
            pokemon_of_p2 = Pokemon(stat_data[3], player2Move)
            pokemon_of_p2.random = reality

        elif player2Index == "4":
            pokemon_of_p2 = Pokemon(stat_data[4], player2Move)
            pokemon_of_p2.random = reality

        rowa= [[pokemon_of_p1.current_hp],[pokemon_of_p2.current_hp]]
        curr_hp_data = open("Pokemon Metadata\\curr_hp.csv", "r")
        curr_hp = list(csv.reader(curr_hp_data, delimiter=","))
        curr_hp_data.close()

        if len(curr_hp)<1:
            print("the 1 time")
            with open('Pokemon Metadata\\curr_hp.csv', 'w', newline='') as filea:
                writer = csv.writer(filea)
                writer.writerow(rowa[0])
                writer.writerow(rowa[1])
            filea.close() 


        return pokemon_of_p1, pokemon_of_p2

    def display_pokemon(self, p1i, p2i):
        '''
        displays the current player's pokemon in the foreground
        '''
        p1display= pg.image.load(self.path+"Sprites\\"+p1i+"B.png").convert()
        p2display= pg.image.load(self.path+"Sprites\\"+p2i+"F.png").convert()


        self.window.display.blit(p1display, (100, 205))
        self.window.display.blit(p2display, (460, 25))
        # self.blit_screen()
        tag_width, tag_height = 800, 600/4+ 30
  
        tag = pg.Rect(0, 435 ,tag_width, tag_height)
        bottom_menu = pg.draw.rect(self.window.display, (253, 216, 53) , tag)
        
        display_tag = pg.Rect(10, 445 ,(tag_width-20), (tag_height-35)/2)
        inset_bottom_menu_t = pg.draw.rect(self.window.display, (255, 255, 255), display_tag)

        self.window.insert_text("Moves:", 20, 57, 445+60 , (26, 35, 126))
        
        move_tag_menu = pg.Rect(10, 445+(tag_height-35)/2 ,(tag_width-20), (tag_height-35)/2)
        pg.draw.rect(self.window.display, (26, 35, 126), move_tag_menu)

    def display_pokemon_info(self, p1, p2, mix_up):
        '''
        Shows the health bar between the two pokemon and displays all pertinent inforation to make the best move
        '''
        curr_hp_data = open("Pokemon Metadata\\curr_hp.csv", "r")
        curr_hp = list(csv.reader(curr_hp_data, delimiter=","))
        curr_hp_data.close()

        if mix_up == 1:
            p2.current_hp=int(curr_hp[0][0])
            p1.current_hp=int(curr_hp[1][0])
        else:
            p1.current_hp=int(curr_hp[0][0])
            p2.current_hp=int(curr_hp[1][0])
        p1rect= pg.Rect(539.4, 348, p1.current_hp*248/p1.max_hp, 12)
        p2rect= pg.Rect(12, 113,    p2.current_hp*248/p2.max_hp, 12)


        underside1= pg.Rect(539.4, 348, 248, 12)
        underside2= pg.Rect(12, 113, 248, 12)
        pg.draw.rect(self.window.display, (41, 48, 40), underside1)
        pg.draw.rect(self.window.display, (41, 48, 40), underside2)


        if p1.current_hp > p1.max_hp/2:
            pg.draw.rect(self.window.display, (92, 158, 92), p1rect)
        
        elif p1.current_hp > p1.max_hp/5:
            pg.draw.rect(self.window.display, (229, 161, 73), p1rect)
        
        else:
            pg.draw.rect(self.window.display, (212, 50, 82), p1rect)

        if p2.current_hp > p2.max_hp/2:
            pg.draw.rect(self.window.display, (92, 158, 92), p2rect)
        
        elif p2.current_hp > p2.max_hp/5:
            pg.draw.rect(self.window.display, (229, 161, 73), p2rect)
        
        else:
            pg.draw.rect(self.window.display, (212, 50, 82), p2rect)

        info_bars=pg.image.load(self.path+"hp-bars.png").convert_alpha()
        self.window.display.blit(info_bars, (0, 0))

        self.window.insert_text(p1.name, 25, 625, 325, self.window.white)
        self.window.insert_text(p2.name, 25, 105, 88, self.window.white)

        self.window.insert_text(str(p2.current_hp)+"/"+str(p2.max_hp), 17, 210, 135, self.window.white)
        self.window.insert_text(str(p1.current_hp)+"/"+str(p1.max_hp), 17, 745, 370, self.window.white)

    def choose_move(self, moves):
        '''
        Creates a colored label in the move selector pool based on the move type.
        '''
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

        self.movebox_width, self.movebox_height = (self.width - 40)/5, (self.height-40)/10
        counter = 0
        for move in moves:
            move_name = move[1]
            move_type = move[2]
            move_box=pg.Rect(60+counter*(self.movebox_width+35), 525 ,self.movebox_width, self.movebox_height)
            if move_type == "Grass":
                pg.draw.rect(self.window.display, grassC, move_box)
                self.window.insert_text(move_name, font_size, 135+counter*(self.movebox_width+35), 553, self.window.black)

            elif move_type == "Fire":
                pg.draw.rect(self.window.display, fireC, move_box)
                self.window.insert_text(move_name, font_size, 135+counter*(self.movebox_width+35), 553, self.window.black)

            elif move_type == "Water":
                pg.draw.rect(self.window.display, waterC, move_box)
                self.window.insert_text(move_name, font_size, 135+counter*(self.movebox_width+35), 553, self.window.white)

            elif move_type == "Ground":
                pg.draw.rect(self.window.display, groundC, move_box)
                self.window.insert_text(move_name, font_size, 135+counter*(self.movebox_width+35), 553, self.window.white)

            elif move_type == "Dragon":
                pg.draw.rect(self.window.display, dragonC, move_box)
                self.window.insert_text(move_name, font_size, 135+counter*(self.movebox_width+35), 553, self.window.white)

            elif move_type == "Ice":
                pg.draw.rect(self.window.display, iceC, move_box)
                self.window.insert_text(move_name, font_size, 135+counter*(self.movebox_width+35), 553, self.window.black)

            elif move_type == "Poison":
                pg.draw.rect(self.window.display, poisonC, move_box)
                self.window.insert_text(move_name, font_size, 135+counter*(self.movebox_width+35), 553, self.window.white)

            elif move_type == "Normal":
                pg.draw.rect(self.window.display, normalC, move_box)
                self.window.insert_text(move_name, font_size, 135+counter*(self.movebox_width+35), 553, self.window.black)

            elif move_type == "Dark":
                pg.draw.rect(self.window.display, darkC, move_box)
                self.window.insert_text(move_name, font_size, 135+counter*(self.movebox_width+35), 553, self.window.white)

            elif move_type == "Flying":
                pg.draw.rect(self.window.display, flyingC, move_box)
                self.window.insert_text(move_name, font_size, 135+counter*(self.movebox_width+35), 553, self.window.black)

            elif move_type == "Steel":
                pg.draw.rect(self.window.display, steelC, move_box)
                self.window.insert_text(move_name, font_size, 135+counter*(self.movebox_width+35), 553, self.window.white)

            elif move_type == "Rock":
                pg.draw.rect(self.window.display, rockC, move_box)
                self.window.insert_text(move_name, font_size, 135+counter*(self.movebox_width+35), 553, self.window.white)

            elif move_type == "Fighting":
                pg.draw.rect(self.window.display, fightC, move_box)
                self.window.insert_text(move_name, font_size, 135+counter*(self.movebox_width+35), 553, self.window.white)

            counter+=1

    def calculatedDMG(self, move, attacking_pkm, defending_pkm):
        move_typing = move[2]
        move_property = move[3]
        move_power = float(move[4])
        move_acc = move[5]
        
        # does the move hit?
        acc_check=random.randint(0, 100)
        try:
            if acc_check > int(move_acc):
                return 0
        except ValueError:
            pass
        # time to check dmg
        if move_property == 'Physical':
            def_power = int(defending_pkm.defense)
            atk_power = int(attacking_pkm.atk)
        else:
            def_power = int(defending_pkm.sdef)
            atk_power = int(attacking_pkm.satk)

        type_csv = open('Pokemon Metadata\\type_effectiveness.csv', 'r')
        type_eff = list(csv.reader(type_csv, delimiter=","))
        type_csv.close()

        # print("type_ef {}", type_eff)
        col_num = 0
        for col in type_eff[0]:
            if col == move_typing:
                break
            col_num += 1
        
        o=0
        for row in type_eff:
            if defending_pkm.typing == [[row[0]], [row[1]]]:
                o=row
                effectiveness = float(row[col_num])
        
        print("col type: {}, row: {}, effectiveness: {}".format( type_eff[0][col_num], o, effectiveness))

        #checks for stab
        if [move_typing] in attacking_pkm.typing:
            is_STAB = 1.5
        else:
            is_STAB = 1

        modifier = random.randint(85, 100)/100
        # dmg = float(float((2*100/5 +2)*float(move_power*float((atk_power//def_power)))//50)*effectiveness*is_STAB)
        dmg = int(((((2*100/5 +2)*move_power*atk_power/def_power)/50)*effectiveness*is_STAB*modifier))
        print (dmg)
        return dmg

        
        


    def check_menu_input(self):
        '''
        changes screens based on the state it is in when a 'enter' key is pressed

        allows for layout to switch whether p1 and p2 is playing with self.phase
        '''
        self.move_menu_cursor()
        if self.window.startKey:
            
            if self.phase == 1:
                self.attacking_move[self.phase]=self.p1.moves[self.state-1]
                self.state = 1
                if self.p2.random == "0":
                    rand_int= random.randint(0, 3)
                    self.attacking_move[2]=self.p2.moves[rand_int]
                    
                else:
                    self.phase = 2
                
            elif self.phase == 2:
                self.attacking_move[self.phase]=self.p2.moves[self.state-1]
                self.phase = 1
                self.state = 1

            print (self.attacking_move)
            self.run_display = False

    def move_menu_cursor(self):
        '''
        based on the directional key presses, changes the state of move choice
        moves cursor based on the state
        '''
        # Right Key
        if self.window.rKey:
            if self.state == self.max_state:
                self.state = 1
                self.tlx = self.width/20
                self.cursor_rect.midtop = (self.tlx, self.tly)
            
            elif self.state == 1:            
                self.state += 1
                self.tlx += (self.movebox_width+35)
                self.cursor_rect.midtop = (self.tlx, self.tly)

            elif self.state == 2:
                self.state += 1
                self.tlx += (self.movebox_width+35)
                self.cursor_rect.midtop = (self.tlx, self.tly)

            elif self.state == 3:
                self.state += 1
                self.tlx += (self.movebox_width+35)
                self.cursor_rect.midtop = (self.tlx, self.tly)


        
        # Left Key
        elif self.window.lKey:
            if self.state == 1:
                self.state = self.max_state
                self.tlx = (self.max_state-1)*(self.movebox_width+35) + self.width/20
                self.cursor_rect.midtop = (self.tlx, self.tly)
            
            elif self.state == 4:            
                self.state -= 1
                self.tlx -= (self.movebox_width+35)
                self.cursor_rect.midtop = (self.tlx, self.tly)

            elif self.state == 3:
                self.state -= 1
                self.tlx -= (self.movebox_width+35)
                self.cursor_rect.midtop = (self.tlx, self.tly)

            elif self.state == 2:
                self.state -= 1
                self.tlx -= (self.movebox_width+35)
                self.cursor_rect.midtop = (self.tlx, self.tly)


