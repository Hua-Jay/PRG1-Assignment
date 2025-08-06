#S10271111E Lee Hua Jay CSF03
from random import randint

player = {}
game_map = []
fog = []
width_counter = 0

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
    player['pickaxe level'] = 0

    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fog
def draw_map(game_map, fog, player):
    map = ''
    for x in range(len(game_map)):
        for y in range(len(game_map[x])):
            if x == player['x'] and y== player['y']:
                map += 'M'
            elif x == 0 and y == 0:
                map += 'T'
            elif fog[x][y] == ' ':
                map += game_map[x][y]
            else:
                map += '?'
        map += '\n'
    return map
def draw_view(game_map, fog, player):
    viewport = ''
    for x in range((0 - player['visibility']), (player['visibility'])):
        for y in range((0 - player['visibility']), (player['visibility'])):
            if x == player['x'] and y == player['y']:
                viewport += 'M'
            else:
                viewport += game_map[x][y]
        viewport += '\n'
    return viewport
initialize_game(game_map, fog, player)
clear_fog(fog, player)
print(draw_view(game_map, fog, player))