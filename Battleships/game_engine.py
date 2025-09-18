import components as cmp

def attack(coordinates, board, battleships):
    #This checks that the current position is in range of the board size and declares a miss if not
    try:
        current = board[coordinates[0]][coordinates[1]]
    except IndexError:
        return False
    
    #This checks to see if a ship is at the current position
    if current == None:
        return False
    else:
        #This reduces the size of the hit ship by 1
        battleships[current] = battleships[current] - 1

        #If the size of the ship is now 0 then it is sunk
        if battleships[current] == 0:
            print("Sunk")

        board[coordinates[0]][coordinates[1]] = None
        return True
    
def cli_coordinates_input():

    #This will loop forever until a valid input is entered
    while True:
        try:
            x = int(input("Enter x coordinate: "))
            y = int(input("Enter y coordinate: "))
            break
        #If the user input is not an integer then a message is output and the loop will continue
        except ValueError:
            print("Coordinates must be integers")
        
    
    return (x, y)

def simple_game_loop():
    #The board is initialised and the ships are placed
    print("Welcome to Battleships")
    board = cmp.initialise_board()
    ships = cmp.create_battleships()
    board = cmp.place_battleships(board, ships)

    won = False

    #This will repeat until the game is won
    while not won:
        #The user inputs the coordinates and these are used for an attack
        coords = cli_coordinates_input()
        shot = attack(coords, board, ships)

        #If it is a hit then "Hit" should be printed and a check needs to be made to see if the game is over
        if shot:
            print("Hit")
            #Assume the game is over
            won = True
            #If there are any ships left with a size that is not 0 then the game is not over
            for value in ships.values():
                if value != 0:
                    won = False
                    break
        else:
            print("Miss")
    
    print("Game over you sunk all the ships")


if __name__ == "__main__":
    simple_game_loop()
        