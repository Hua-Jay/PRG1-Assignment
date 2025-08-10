#S10271111E Lee Hua Jay CSF03
from random import randint
#shows high score list
try:
    scoresheet = open('sundropcaveshighscores.txt','r')
    high_scores = scoresheet.read().split('\n')
    scoresheet.close()
except FileNotFoundError or len(high_scores) == 0:
    high_scores = []

player = {}
game_map = []
fog = []
ore = ['copper','silver','gold']
#list of valid inputs for each menu, excluding valid_buys
valid_mainmenu = ['N', 'L', 'H', 'Q']
valid_townmenu = ['B', 'I', 'M', 'E', 'V', 'Q']
valid_warehouse = ['C', 'S', 'G', 'L']

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    map_file = open(filename, 'r')
    global MAP_WIDTH
    global MAP_HEIGHT
    
    map_struct.clear()
    
    # TODO: Add your map loading code here
    map_levels = map_file.read().split('\n')
    for level in map_levels:
        map_struct.append(level)
    
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    for level in range(len(fog)):
        for width in range(len(fog[level])):
            if (level >= (player['y'] - player['visibility']) and level <= (player['y'] + player['visibility'])) and (width >= (player['x'] - player['visibility']) and width <= (player['x'] + player['visibility'])):
                fog[level][width] = ' '
    return

def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)

    # TODO: initialize fog
    fog.clear()
    for i in range(MAP_HEIGHT):
        fog_layer = []
        for j in range(MAP_WIDTH):
            fog_layer.append('?')
        fog.append(fog_layer)

    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['visibility'] = 1
    player['pickaxe_level'] = 1
    player['max_load'] = 10
    player['current_load'] = 0
    player['state'] = 'main'
    name = input('Greetings, miner! What is your name? ')
    while name == '\n===\n':
        name = input('Your name reminds the mining gods of a shameful past. Through divine intervention, you are made to change your name to: ')
    player['name'] = name
    print('Pleased to meet you, {}. Welcome to Sundrop Town!'.format(name))

    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fog
def draw_map(game_map, fog, player):
    map = '+' + '-'*len(game_map[0]) + '+\n'
    for x in range(len(game_map)):
        map += '|'
        for y in range(len(game_map[x])):
            if x == player['x'] and y== player['y']:
                map += 'M'
            elif x == 0 and y == 0:
                map += 'T'
            elif fog[x][y] == ' ':
                map += game_map[x][y]
            else:
                map += '?'
        map += '|\n'
    map += '+' + '-'*len(game_map[0]) + '+'
    return map

# This function draws the 3x3 viewport, changed to 5x5 if torch is bought (visibility will +1)
def draw_view(game_map, fog, player):
    viewport = '+' + '-'*(player['visibility']*2 + 1) + '+\n'
    for y in range((player['y'] - player['visibility']), (player['y'] + player['visibility'] + 1)):
        viewport += '|'
        if y < 0 or y > MAP_HEIGHT:
            viewport += '#' * ((2 * player['visibility']) + 1)
        else:
            for x in range((player['x'] - player['visibility']), (player['x'] + player['visibility'] + 1)):
                if x == player['x'] and y == player['y']:
                    viewport += 'M'
                elif x < 0 or x > MAP_WIDTH:
                    viewport += '#'
                else:
                    viewport += game_map[y][x]
        viewport += '|\n'
    viewport += '+' + '-'*(player['visibility']*2 + 1) + '+'
    return viewport

# This function shows the information for the player
def show_information(player):
    print('----- Player Information -----\nName: {}\nCurrent Position: ({},{})\nPickaxe Level: {}\nGold: {}\nSilver: {}\nCopper: {}\n------------------------------\n\
          Load: {}/{}\n------------------------------\nGP: {}\nSteps Taken: {}\n------------------------------'.format(\
              player['name'],player['x'], player['y'], player['pickaxe_level'], player['gold'], player['silver'], player['copper'],\
                 player['current_load'], player['max_load'], player['GP'], player['steps']))
    return

# This function saves the game
def save_game(game_map, fog, player):
    gamedata = [game_map, fog]
    file = open('SaveFile.txt', "w")
    #save game_map and fog
    for type in range(2):
        for row in gamedata[type]:
            line = ''
            for i in range(len(row)):
                line += str(row[i])
                if i < (len(row) - 1):
                    line += ","
            file.write(line + "\n")
        file.write('===\n')#add seperator
    #save player
    for key in player:
        file.write(str(key) + ":" + str(player[key]) + "\n")
    file.close()
    return 'Game saved.'
        
# This function loads the game
def load_game(game_map, fog, player):
    loaded_data = []
    #remove previous data
    game_map.clear()
    fog.clear()
    player.clear()
    #read save file
    try:
        file = open('SaveFile.txt', "r")
        dataread = file.read().split('\n===\n')#splits with seperator
        file.close()
    except FileNotFoundError:
        print('Save file empty. Game will be initialized instead')
        initialize_game(game_map, fog, player)
        return
    if dataread == []:
        print('Save file empty. Game will be initialized instead')
        initialize_game(game_map, fog, player)
        return
    #save game_map and fog
    for i in range(2):
        new_data = []
        for data in dataread[i].split('\n'):
            new_data.append(data)
        loaded_data.append(new_data)
    game_map = loaded_data[0]
    fog = loaded_data[1]
    #save player
    for line in dataread[2].strip().split('\n'):
        if ':' in line:
            key, value = line.split(':')
    #convert numbers to int
            if value.isdigit():
                value = int(value)
            player[key] = value
    print('Game Loaded.')
    return

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

#this function opens the town menu
def show_town_menu(player):
    print()
    print('Day {}'.format(player['day']))
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print('(A)ccess Warehouse')
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")

#this function opens the shop menu
def show_shop_menu(player):
    buyables = 0
    global valid_buys
    valid_buys = ['L']
    print()
    print('----------------------- Shop Menu -------------------------')
    if player['pickaxe_level'] < 3:
        buyables += 1
        valid_buys.append('P')
        print('(P)ickaxe upgrade to level {} to mine {} ore for {} GP'.format(player['pickaxe_level'] + 1,ore[player['pickaxe_level']], pickaxe_price[player['pickaxe_level'] - 1]))
    if player['max_load'] < 20: #max steps is 20 per day, so only 20 is needed 
        buyables += 1
        valid_buys.append('B')
        print('(B)ackpack upgrade to carry {} items for {} GP'.format(player['max_load'] + 2, player['max_load'] * 2))
    if player['visibility'] == 1:
        buyables += 1
        valid_buys.append('T')
        print('Magic (T)orch to increase visiblity to a 5x5 box for 50 GP')
    if buyables == 0:
        print('You currently have the best possible equipment!')
    print('(L)eave shop')
    print('-----------------------------------------------------------')
    print('GP: {}'.format(player['GP']))
    print('-----------------------------------------------------------')

#this function updates the high score list at the end of every playthrough
def show_high_scores(high_scores):
    print()
    print('------------- High Scores -------------')
    if len(high_scores) == 0:
        print('The scoreboard is empty. Be here soon?')
    else:
        for placing in range(len(high_scores)):
            print('{}. {} - {} days - {} steps'.format(placing + 1, high_scores[placing][0], high_scores[placing][1], high_scores[placing][2]))
    print('---------------------------------------')

#to be used at end of each win
def update_scores(player, high_scores):
    formatted_score = [player['name'], player['day'], player['steps'], player['GP']]
    if len(high_scores) == 0: #checks if 
        high_scores.append(formatted_score)
    else:
        for placing in range(len(high_scores)):
            for tiebreak in range(1, 4):
                if formatted_score[tiebreak] < (high_scores[placing])[tiebreak]:
                    break
                elif formatted_score[tiebreak] > (high_scores[placing])[tiebreak]:
                    high_scores.insert(placing, formatted_score)
                    if len(high_scores) > 5:
                        high_scores.pop()
                    return
        if len(high_scores) < 5:
            high_scores.append(formatted_score)
                
def valid_input(valids, user_input): #function for validity checking
    while user_input not in valids: #loops if input isn't in list of valid inputs
        user_input = input('Invalid input. Please enter a valid key: ')
    return user_input
#this function responds to possible player actions in the main menu
def menu_options():
    show_main_menu()
    choice = input('Your choice? ').upper()
    valid_input(valid_mainmenu, choice)
    if choice == 'N':
        initialize_game(game_map, fog, player)
    elif choice == 'L':
        load_game(game_map, fog, player)
    elif choice == 'H':
        show_high_scores(high_scores)
        menu_options()
    else:
        quit()

#this function responds to possible player actions in the shop
def shop_options(player):
    show_shop_menu(player)
    choice = input('Your choice? ').upper()
    choice = valid_input(valid_buys, choice)
    while choice != 'L':
        if choice == 'P':
            if player['GP'] >= pickaxe_price[player['pickaxe_level'] - 1]:
                player['GP'] -= pickaxe_price[player['pickaxe_level'] - 1]
                player['pickaxe_level'] += 1
                print('Congratulations! You can now mine {}!'.format(ore[player['pickaxe_level']]))
        elif choice == 'B':
            if player['GP'] >= (player['max_load'] * 2):
                player['GP'] -= (player['max_load'] * 2)
                player['max_load'] += 2
                print('Congratulations! You can now carry {} items!'.format(player['max_load']))
        elif choice == 'T':
            if player['GP'] >= 50:
                player['GP'] -= 50
                player['visibility'] += 1
                print('Congratulations! Your view range has increased to a 5x5 square!')
        else:
            print('Insufficient GP. Sell ores for more GP!')
        show_shop_menu(player)
        choice = input('Your choice? ').upper()
        choice = valid_input(valid_buys, choice)
        

#displays the warehouse
def show_warehouse(player):
    print('------------------------ Warehouse ------------------------')
    print('Ores stored in warehouse:\n')
    print('Copper: ' + str(player['copper']))
    print('Silver: ' + str(player['silver']))
    print('Gold: ' + str(player['gold']))
    print('Today\'s ore prices:\n')
    print('Copper: ' + str(copper_price))
    print('Silver: ' + str(silver_price))
    print('Gold: ' + str(gold_price) +'\n')
    print('Sell (C)opper\nSell (S)ilver\nSell (G)old\n(L)eave warehouse')
    print("-----------------------------------------------------------")

#this function responds to possible player actions in the warehouse
def warehouse_options(player):
    choice = ''
    while choice != 'L':
        if choice == 'C':
            if player['copper'] > 0:
                player['GP'] += copper_price * player['copper']
                print('\nYou have sold {} copper for {} GP!'.format(player['copper'], (copper_price * player['copper'])))
                player['copper'] = 0
            else:
                print('\nYou have 0 copper to sell. Find more in the mines!')
        elif choice == 'S':
            if player['Silver'] > 0:
                player['GP'] += silver_price * player['silver']
                print('\nYou have sold {} silver for {} GP!'.format(player['silver'], (silver_price * player['silver'])))
                player['silver'] = 0
            else:
                print('\nYou have 0 silver to sell. Find more in the mines!')
        elif choice == 'G':
            if player['gold'] > 0:
                player['GP'] += gold_price * player['gold']
                print('\nYou have sold {} gold for {} GP!'.format(player['gold'], (gold_price * player['gold'])))
                player['gold'] = 0
            else:
                print('\nYou have 0 gold to sell. Find more in the mines!')
        show_warehouse(player)
        choice = input('Your choice? ').upper()
        choice = valid_input(valid_warehouse, choice)

#--------------------------- MAIN GAME ---------------------------
player['state'] = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 500 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!
menu_options()
while player['GP'] < 500:
    if player['state'] == 'main':
        player['day'] += 1
    copper_price = randint(1, 3)
    silver_price = randint(5, 8)
    gold_price = randint(10, 18)
    choice = ''
    player['state'] = 'town'
    if player['state'] == 'town':
        while choice != 'E':
            if choice == 'Q':
                quit()
            elif choice == 'B':
                shop_options(player)
            elif choice == 'M':
                print(draw_map(game_map, fog, player))
            elif choice == 'V':
                save_game(game_map, fog, player)
            elif choice == 'A':
                warehouse_options(player)
            elif choice == 'I':
                show_information(player)
            show_town_menu(player)
            choice = input('Your choice? ').upper()
    player['state'] = 'mines'
    
