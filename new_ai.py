#from re import I
#from syslog import LOG_LOCAL0
import copy
#from tetris import Figure

def collision_check(playField, figure, xpos, ypos): 
    #copied code from tetris.py and modified it (changed variable names) for our use.
    #xpos and ypos are position of the figure on the playField

    intersection = False
    intersectionType = "none"

    height = len(playField)
    width = len(playField[0])

    #print("xpos:", xpos, "ypos:", ypos)
    #print("height:", height, "width:", width)

    for i in range(4):
        for j in range(4):
            if i * 4 + j in figure:
                if j + xpos > (width-1) or j + xpos < 0 :
                    intersection = True
                    intersectionType = "wall"
                elif i + ypos > (height-1):
                    intersection = True
                    intersectionType = "floor"
                elif playField[i + ypos][j + xpos] > 0:
                    intersection = True
                    intersectionType = "block"
                    
    return (intersection, intersectionType)

def h_generate_positions(playField, figure):

    fieldHeight = len(playField)
    fieldWidth = len(playField[0])
    validPositions = []
    previousPosition = (None, None)
    
    # x (column) starts at -1 and ends at the field size
    for x in range(-1,fieldWidth): #columns
        for y in range(0,fieldHeight): #rows
            currentPosition=(x,y)
            collisionTuple = collision_check(playField, figure, currentPosition[0], currentPosition[1])
            collision = collisionTuple[0]
            collisionType = collisionTuple[1]
            #print("currentPosition:", currentPosition, "collision:",collisionTuple)
           
            #what happens if you hit a block straight off and previousPosition is undefined?
            
            if (collision):
                if (collisionType == 'block' or collisionType == "floor"):
                    validPositions.append(previousPosition)
                break
            else:
                previousPosition = currentPosition
            previousPosition = currentPosition
                
    return validPositions

def generate_all_positions(playField, figures):
    allPositions = []
    
    for figure in figures:
        #print("Figure:", figure)
        positions = h_generate_positions(playField, figure)
        allPositions.append(copy.deepcopy(positions))
    
    return allPositions

def place_on_playfield(oldPlayField, figure, position):

    newplayField = copy.deepcopy(oldPlayField)
    #print ("figure: ", figure)
    #print ("position:", position)

    for i in range(4):  # y (columns)
        for j in range(4): # x (rows)
            if i * 4 + j in figure:
                #print ("i: ", (i+position[1]), " j:", (j+position[0]))
                newplayField[i + position[1]][j + position[0]] = 2

    return newplayField
    

def find_best_place (playField, figureR, weights=[0.25,0.25,0.25,0.25]):  #weights to be passed to f()
    """Function to evaluate the different possible positions and find the best according to the modifiers
        Returns the position of the best placement from a list of positions"""
    # takes data from generate_positions and returns the best position using f()
    #if weights is None:
    #    weights = [0.25, 0.25, 0.25, 0.25]
    placements = []  
        
    #print ("Weights: ", weights)
    
    # find all the valid places
    validPositions = generate_all_positions(playField, figureR)
    
    #print("Valid Positions returned to fbp: ", validPositions)

    if validPositions == []:
        #print("no valid positions")
        return [-1,-1]

    # iterate through the validPositions list. deal with each rotations separately.

    # need to deal with an empty set as well. probably use an "if" statement

    numRotations = len(validPositions)
    for rotation in range(numRotations):
        for position in validPositions[rotation]:
            figure = figureR[rotation]
            
            #print("position:", position, "rotation:", rotation, "numRotations", numRotations)
            if position != (None, None):
                newPlayfield = place_on_playfield(playField, figure, position)
            
                '''
                print("newPlayField")
                for row in newPlayfield:
                    print(row)
                '''
                
                aggHeight = aggregate_height(newPlayfield)
                numHoles = count_holes(newPlayfield, aggHeight)  
                amtBumpy = bumpiness(newPlayfield)
                completedLines = completed_lines(newPlayfield)

                placementScore = f(aggHeight, numHoles, amtBumpy, completedLines, weights, position[1]) 

                placement = [rotation, position]
                placements.append([placementScore, placement])

    # find the best (lowest) scoring placement and return that

    # Can you believe that there is a case that there are NO valid positions?
    if placements == []:
        return [0,(3,0)]

    bestPlacement = placements[0][1]
    bestScore = placements[0][0]

    for placement in placements:
        if (placement[0] < bestScore):
            bestPlacement = placement[1]  # [r,[x,y]]
            bestScore = placement[0]

    #print("Best score+placement: " , placement, " Returning: ", bestPlacement)
    #print("ah:", aggHeight, "ho:", numHoles, "bu:", amtBumpy, "cl:", completedLines, "sc:", placementScore)
    return  bestPlacement  # best place returned


def f(aggHeight, numHoles, amtBumpy, completedLines, weights=[0.25,0.25,0.25,0.25], row=20):
    """The evaluation function of a state
        Returns a value 0<x<10? on how good the state is"""
    # decision based on statistics

    score = ((aggHeight) * weights[0]) + ((numHoles) * weights[1]) + ((amtBumpy) * weights[2]) + ( ((4 - completedLines)) * weights[3])

    #score = ((aggHeight**2) * weights[0]) + ((numHoles**4) * weights[1]) + ((amtBumpy**2) * weights[2]) + ( ((4 - completedLines)**5) * weights[3])
    #score += ((5*(20-row)))
    
    return score


def set_mod():
    """Change the modifiers used to the new values"""


def run_ai():
    """Driver class
        Input: figure, field
        Returns the position for the figure
        (Potential for mutil threading for time limit but this is extra)"""

def aggregate_height(playField):
    # Calculate aggregate height
    # Argument: array (play field)
    # Returns: integer (aggregate height)

    # The height of each column is the actual height - number of zeros (excl. holes)
    # so, count the zeros, subtract the total number of holes, then
    # subtract that number from the total number of cells which can be calculated
    # by the length of the list of lists times the length of the inside lists.

    numRows = len(playField)
    numCols = len(playField[0])
    zerocount = 0
    aggHeight = 0
    
    for i in range(numCols):
        for j in range(numRows):

            if (playField[j][i] == 0):
                zerocount += 1
            else:
                break

        aggHeight += (numRows - zerocount)
        zerocount = 0

    return (aggHeight)

def count_holes(playField, aggregateHeight = -1 ):
    # count the number of holes in the playField
    # holes are defined as infilled cells that cannot be accessed.
    # For this, we determine how many empty cells are in the entire playfield
    # then we subtract the total number of cells and add back in the aggregate height
    # this gives us an admittedly inaccurate, but close, number of holes.

    zeroCount = 0
    hole = 0
    holeCount = 0
    
    totalCells = len(playField) * len(playField[0])

    for row in playField:
        zeroCount += row.count(hole)

    if (aggregateHeight < 0):
        holeCount = zeroCount - ( totalCells - aggregate_height(playField) )
    else:
        holeCount = zeroCount - ( totalCells - aggregateHeight )

    return holeCount

def bumpiness(playField):
    #
    # return an array the same length of the number of columns
    # first n entries are the differences between adjacent columns.
    # the final entry is the average bumpiness or sum of the bumpiness
    numRows = len(playField)
    numCols = len(playField[0])
    bumpiness = [0] * numCols
    sum = 0
    
    
    for i in range(numCols):
        for j in range(numRows):
            if(playField[j][i] != 0): # corrected this line. 0 indicates empty. a full space can be 1 through 9
                bumpiness[i] = numRows - j #gets the position of the highest point of each column
                break
    i = 0
    while i < len(bumpiness)-1:
        bumpiness[i] = (abs(bumpiness[i] - bumpiness[i+1]))**2 #finds delta of each column
        sum += bumpiness[i]
        i+=1
    
    #bumpiness[i] = sum #/(len(bumpiness)-1) #provides the average bumpiness
    #print ("bumpiness: ", bumpiness)
    #return bumpiness
    return sum

def completed_lines(playField): 
    # 
    # applied once a piece is placed.
    # look for lines that have no empty cells
    
    numRows = len(playField)
    numCols = len(playField[0])
    compLines = 0
    for i in range(numRows):
        line = True
        for j in range(numCols):
            if(playField[i][j] == 0):
                line = False
                break
        if(line == True):
            compLines+=1
    return compLines
