import new_ai as nai


figures = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[4, 5, 9, 10], [2, 6, 5, 9]],
    [[6, 7, 9, 10], [1, 5, 6, 10]],
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    [[1, 2, 5, 6]],
]

playField0 = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
]

# aggregate height = 11 + 8 + 3 + 3 + 3 + 6 + 4 + 4 + 4 + 4 = 50
# holes = 1 + 1 + 1 + 1 + 1 + 1 = 6
# completed lines = 0
# bumpiness = [3, 5, 0, 0, 3, 2, 0, 0, 0, 13]
playField1 = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1],
    [0,1,0,0,0,1,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,0,0,0],
    [1,1,1,1,1,1,0,1,1,0],
    [1,1,0,1,1,1,1,1,1,0]
]

# aggregate height = 11 + 8 + 3 + 3 + 3 + 6 + 4 + 4 + 4 + 4 = 50
# holes = 1 + 1 + 0 + 0 + 0 + 0 + 1 + 0 + 0 + 0 = 3
# completed lines = 2
# bumpiness = [3, 5, 0, 0, 3, 2, 0, 0, 0, 13]
playField2 = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,1,0,0,0,0],
    [1,1,0,0,0,1,0,0,0,0],
    [1,0,0,0,1,1,1,1,1,1],
    [1,1,1,1,1,0,0,0,1,1],
    [1,1,1,1,1,0,0,0,1,1],
    [1,1,1,1,1,0,0,0,1,1]
]

playField3 = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,1,1,1,1,1,1],
    [1,1,1,1,1,0,0,0,1,1],
    [1,1,1,1,1,0,0,0,1,1],
    [1,1,1,1,1,0,0,0,1,1],
    [1,0,0,0,1,1,1,1,1,1],
    [1,1,1,1,1,0,0,0,1,1],
    [1,1,1,1,1,0,0,0,1,1],
    [1,1,1,1,1,0,0,0,1,1],
    [1,0,0,0,1,1,1,1,1,1],
    [1,1,1,1,1,0,0,0,1,1],
    [1,1,1,1,1,0,0,0,1,1],
    [1,1,1,1,1,0,0,0,1,1],
    [1,0,0,0,1,1,1,1,1,1],
    [1,1,1,1,1,0,0,0,1,1],
    [1,1,1,1,1,0,0,0,1,1],
    [1,1,1,1,1,0,0,0,1,1]
]

fieldInPlay = playField0
figure = figures[0]
rotation = 0
position = [2,16]

for row in fieldInPlay:
    print(row)

print(nai.collision_check(fieldInPlay, figure[rotation], position[0], position[1]))

newPlayfield = nai.place_on_playfield(fieldInPlay, figure, rotation, position)

for row in newPlayfield:
    print(row)

'''
bestPlace = nai.find_best_place(fieldInPlay, figure)
print ("Best Position [r,[x,y]]: ", bestPlace)

print("figure: ", figure)
print("rotation: ", bestPlace[0])
print("position: ", bestPlace[1])

newPlayfield = nai.place_on_playfield(fieldInPlay, figure, bestPlace[0], bestPlace[1])

print ("NewplayField")
for row in newPlayfield:
    print(row)

aggHeight = nai.aggregate_height(newPlayfield)
numHoles  = nai.count_holes(newPlayfield)

print("Aggregate Height: ", aggHeight)
print("Number of Holes: ", numHoles)

positions = nai.h_generate_positions(newPlayfield, figure)
numRotations = len(positions)
print("Number of Rotations: ", numRotations)
print("Positions: ", positions)

amtBumpy = nai.bumpiness(newPlayfield)
print("Bumpiness :" , amtBumpy)

completedLines = nai.completed_lines(newPlayfield)
print("Completed Lines: " , completedLines)

score = nai.f(aggHeight, numHoles, amtBumpy, completedLines)
print("Score: ", score)
'''