#S10271111E Lee Hua Jay CSF03
from random import randint

player = {}
game_map = []
fog = []
width_counter = 0
current_load = 0

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
    player['name'] = ''
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['visibility'] = 1
    player['pickaxe level'] = 0
    player['load'] = 10

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

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    viewport = '+' + '-'*(player['visibility']*2 + 1) + '+\n'
    for x in range((player['x'] - player['visibility']), (player['x'] + player['visibility'] + 1)):
        if x < 0:
            continue
        else:
            viewport += '|'
            for y in range((player['y'] - player['visibility']), (player['y'] + player['visibility'] + 1)):
                if x == player['x'] and y == player['y']:
                    viewport += 'M'
                elif y < 0:
                    continue
                else:
                    viewport += game_map[x][y]
            viewport += '|\n'
    viewport += '+' + '-'*(player['visibility']*2 + 1) + '+'
    return viewport

# This function shows the information for the player
def show_information(player):
    print('----- Player Information -----\nName: {}\nCurrent Position: ({},{})\nPickaxe Level: {}\nGold: {}\nSilver: {}\nCopper: {}\n------------------------------\n\
          Load: {}/{}\n------------------------------\nGP: {}\nSteps Taken: {}\n------------------------------'.format(\
              player['name'],player['x'], player['y'], player['pickaxe level'], player['gold'], player['silver'], player['copper'],\
                 current_load, player['load'], player['GP'], player['steps']))
    return #TODO add day info

# This function saves the game
def save_game(game_map, fog, player):
    global SAVED_MAP
    global SAVED_FOG
    global SAVED_PLAYER
    # save map
    SAVED_MAP = game_map
    # save fog
    SAVED_FOG = fog
    # save player
    SAVED_PLAYER = player
    return
        
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    game_map = SAVED_MAP
    # load fog
    fog = SAVED_FOG
    # load player
    player = SAVED_PLAYER
    return

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
#    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    print()
    # TODO: Show Day
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")
            
def valid_input(valids, user_input): #function for validity checking
    while user_input not in valids: #loops if input isn't in list of valid inputs
        user_input = input('Invalid input. Please enter a valid key: ')
    return user_input

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!
    
    
