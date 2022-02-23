from cmath import inf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import hsv_to_rgb
import math
import random
import heapq
import bisect
import random

# initialize parameters
height = 50;    # map height
width = 50      # map width
num_bots = 15   # number of bots
max_itr = 2500  # maximum number of iterations

wall = 1        # value for a wall in the map matrix
mapped = .4     # value for a mapped area in map matrix
planned = .2    # value for a bot's planned path in map matrix
unmapped = 0    # value for a unmapped area in map matrix

# define structure to hold all information about the bots and map
bots = [{} for i in range(num_bots)]

# define the provided blueprint map
blueprint = np.pad(np.zeros((height-2,width-2)), (1,1), 'constant', constant_values = (wall, wall)) # a map provided to the bot network
blueprint[9:19,35] = wall
blueprint[9:19,44] = wall
blueprint[9,35:37] = wall
blueprint[9,42:44] = wall
blueprint[19,35:44] = wall

# define the bot's map of explored areas
explore_map = blueprint; # a map the bot network uses to keep track of where bots have visited

# initialize positions, dest, route, and exploration map
for i in range(num_bots):
    bots[i]['current_position'] = [math.floor(height/2), math.floor(width/2)]
    explore_map[bots[i]['current_position'][0], bots[i]['current_position'][1]] = mapped
    bots[i]['destination'] = [] 
    bots[i]['route'] = [] 

plt.imshow(explore_map, cmap='gray')
plt.title('Press \'q\' button to begin.')
plt.show()


# returns a Nx2 matrix where N is the number of locations the bots have not explored
def get_unexplored_areas(explore_map, unmapped):
    return list(zip(*np.where(explore_map==unmapped)))


# pick the closest unexplored area as the new destination dest.
def get_new_destination(position, unexplored_areas):
    options = [[inf, position]]
    for location in unexplored_areas:
        distance = np.linalg.norm(np.array(location)-position)
        if distance <= options[0][0]:
            bisect.insort(options, [distance, location])
            while options[-1][0] > options[0][0]: 
                options.pop()    
                
    return random.choice(options)[1]
    

# marks locations in route as PLANNED 
def update_explore_map(dest, route, explore_map, planned, unmapped):
    for x, y in route:
        if explore_map[x][y] == unmapped:
            explore_map[x][y] = planned
    
    return explore_map


# moves the current position one step closer to the destination
def update_position(curPos, route, dest, explore_map, mapped):
    for i in range(len(route)):
        if all(route[i]==curPos):
            route = np.delete(route, i, 0)
            break
    
    minDistance = inf
    for location in route:
        distance = np.linalg.norm(location-curPos)
        if distance < minDistance:
            curPos = location
            minDistance = distance

    explore_map[curPos[0]][curPos[1]] = mapped
    
    if curPos[0]==dest[0] and curPos[1]==dest[1] :
        dest = []

    return curPos, route, dest, explore_map


def update_bot_info(curPos, dest, route, explore_map, botNum):
    bots[botNum]['current_position'] = curPos
    bots[botNum]['destination'] = dest
    bots[botNum]['route'] = route
    explore_map = explore_map


# heuristic function for path scoring
def heuristic(a, b):
    return np.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)


def a_star(array, start, goal):    
    start = tuple(start)
    goal = tuple(goal)

    neighbors = [(0,1),(0,-1),(1,0),(-1,0)]
    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}

    oheap = []
    heapq.heappush(oheap, (fscore[start], start))
 
    while oheap:

        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(list(current))
                current = came_from[current]
            return np.array(data)

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j

            tentative_g_score = gscore[current] + heuristic(current, neighbor)

            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
 
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:

                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))
 
    return False


for itr in range(max_itr):
    for botNum in range(num_bots):
        # extract bot's info for convenience/code readability
        curPos = bots[botNum]['current_position']
        dest = bots[botNum]['destination']
        route = bots[botNum]['route']

        # if the bot doesn't have a destination then pick a new destination
        if len(dest) == 0: 
                    
            # get the locations of all areas that are labeled as unmapped 
            # TODO: write this function above.
            unexplored_areas = get_unexplored_areas(explore_map, unmapped)
            
            # if there are no more unexplored areas, then this bot stops moving
            if len(unexplored_areas) == 0:
                dest = []
                route = []
                update_bot_info(curPos, dest, route, explore_map, botNum)
                continue
            
            # calculate bot's new destination (TODO: write this function above)
            dest = get_new_destination(curPos, unexplored_areas)
            
            # calculates bot's route to the destination (you do not need to worry about this function)
            if a_star(explore_map, curPos, dest).size:
                route = a_star(explore_map, curPos, dest)
                route = np.vstack((route, curPos))
                route = route[::-1]

            
            # mark the location in explored_map as planned if it was unmapped (TODO: write this function above)
            explore_map = update_explore_map(dest, route, explore_map, planned, unmapped)

        # Using the calculated route, move the bot 1 step towards the destination bot's destination (TODO: write this function above)
        curPos, route, dest, explore_map = update_position(curPos, route, dest, explore_map, mapped)
        
        # update bot's curr position, past position, destination, and map
        update_bot_info(curPos, dest, route, explore_map, botNum)

    # update display
    plt.imshow(explore_map, cmap='gray')
    for i in range(num_bots):
        c = hsv_to_rgb([i/num_bots, 1, 1])
        fig = plt.gcf()
        ax = fig.gca()
        ax.add_patch(patches.Rectangle((bots[i]['current_position'][1]-.5, bots[i]['current_position'][0]-.5), 1, 1, edgecolor=c, facecolor=c, fill=True))
        #if len(bots[i]['destination']) != 0:
        #    plt.plot([b[1] for b in bots[i]['route']], [b[0] for b in bots[i]['route']], color='red')
        #    plt.plot(bots[i]['destination'][1], bots[i]['destination'][0], color='yellow')

    plt.show(block=False)
    plt.pause(.0001)
    ax.patches.clear()
    mapped_count = sum(sum(np.array(explore_map) == mapped))
    wall_count = sum(sum(np.array(explore_map) == wall))
    explore_size = explore_map.size
    if (mapped_count + wall_count) == explore_size:
        break

print("Number of iterations: "+str(itr))