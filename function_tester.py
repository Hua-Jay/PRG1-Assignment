#S10271111E Lee Hua Jay CSF03
#here I test every function I am writing for the assignment
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

def show_information(player):
    print('----- Player Information -----\nName: {}\nCurrent Position: ({},{})\nPickaxe Level: {}\nGold: {}\nSilver: {}\nCopper: {}\n------------------------------\n\
          Load: {}/{}\n------------------------------\nGP: {}\nSteps Taken: {}\n------------------------------'.format(\
              player['name'],player['x'], player['y'], player['pickaxe level'], player['gold'], player['silver'], player['copper'],\
                 current_load, player['load'], player['GP'], player['steps']))
    return #TODO add day info
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
    player['name'] = 'tes'
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
    map += '+' + '-'*len(game_map[0]) + '+\n'
    return map

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



def valid_input(valids, user_input): #function for validity checking
    while user_input not in valids: #loops if input isn't in list of valid inputs
        user_input = input('Invalid input. Please enter a valid key: ')
    return user_input
initialize_game(game_map, fog, player)

def show_high_scores(high_scores):
    print()
    print('------------- High Scores -------------')
    for placing in range(5):
        print('{}. {} - {} days - {} steps'.format(placing + 1, high_scores[placing][0], high_scores[placing][1], high_scores[placing][2]))
    print('---------------------------------------')

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
def save_game(game_map, fog, player):
    gamedata = [game_map, fog]
    file = open('SaveFile.txt', "w")
    for type in range(2):
        for row in gamedata[type]:
            line = ''
            for i in range(len(row)):
                line += str(row[i])
                if i < (len(row) - 1):
                    line += ","
            file.write(line + "\n")
        file.write('===\n')
    for key in player:
        file.write(str(key) + ":" + str(player[key]) + "\n")
    file.close()
    return 'Game saved.'

def load_game(game_map, fog, player):
    loaded_data = []

    #remove previous data
    game_map.clear()
    fog.clear()
    player.clear()
    #read save file
    file = open('SaveFile.txt', "r")
    dataread = file.read().split('\n===\n')#splits with seperator
    file.close()
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
    return
player['name'] = 'tester'
save_game(game_map,fog,player)
initialize_game(game_map, fog, player)
load_game(game_map, fog, player)
print(player)