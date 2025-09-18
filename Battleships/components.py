import random
import json

def initialise_board(size=10):
    return [[None for i in range(size)] for j in range(size)]

def create_battleships(filename="battleships.txt"):
    ships = {}

    with open(filename, "r") as file:
        for line in file:
            #Ships are stored in a csv format so the name and the size are seperated by a comma
            values = line.strip().split(",")
            ships[values[0]] = int(values[1])
    
    return ships
    
def place_battleships(board, ships, algorithm="simple"):
    size = len(board[0])
    counter = -1
    #This loops through every item in the ships dictionary
    for key, value in ships.items():
        counter += 1
        placed = False

        #This checks what type of placement algorithm should be used
        if algorithm == "custom":
            #The json file contains the starting coordinates and orientation of each ship so these values are read in
            with open("placement.json", "r") as file:
                dict = json.load(file)
                ship = dict[key]
                row = int(ship[1])
                column = int(ship[0])
                horizontal = ship[2]

        elif algorithm == "random":
            #This will try to place the ships until it finds a position that the ship can fit into
            while not placed:
                #This randomly picks the orientaiton of the ship
                horizontal = random.choice(["h", "v"])
                #This checks the orientation of the ship
                if horizontal == "h":
                    #Coordinates for the start of the ship are randomly chosen
                    row = random.randint(0, size-1)
                    column = random.randint(0, size-value)
                    #This checks the place the ship will be placed is empty
                    placed = True
                    for i in range(value):
                        if board[row][column+i] != None:
                            placed = False
                            break
                    
                else:
                    #Coordinates for the start of the ship are randomly chosen
                    row = random.randint(0, size-value)
                    column = random.randint(0, size-1)
                    #This checks the place the ship will be placed is empty
                    placed = True
                    for i in range(value):
                        if board[row+i][column] != None:
                            placed = False
                            break
        else:
            #The simple algoithm is the one that is used if the user does not provide a valid algorithm
            row = counter
            column = 0
            horizontal = "h"
        
        #This places the ship in the designated place
        if horizontal == "h":
            for i in range(value):
                try:
                    board[row][column+i] = key
                except IndexError:
                    print("Placement file not valid, please change it")
                    exit()
        else:
            for i in range(value):
                try:
                    board[row+i][column] = key
                except IndexError:
                    print("Placement file not valid, please change it")
                    exit()


    return board

