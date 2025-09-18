import random
import components as cmp
import game_engine as ge

players = {}

def generate_attack(size=10):
    x = random.randint(0, size)
    y = random.randint(0, size)

    return (x, y)

def ai_opponent_game_loop():
    print("Welcome to battleships")

    #Initialise player variables
    playerBoard = cmp.initialise_board()
    playerShips = cmp.create_battleships()
    playerBoard = cmp.place_battleships(playerBoard, playerShips, "custom")
    players["player"] = [playerBoard, playerShips]

    size = len(playerBoard[0])

    #initialise AI variables
    aiBoard = cmp.initialise_board()
    aiShips = cmp.create_battleships()
    aiBoard = cmp.place_battleships(aiBoard, aiShips, "random")
    players["ai"] = [aiBoard, aiShips]

    won = False
    gameOver = False

    while not gameOver:
        #Player's turn
        print("\n\nPlayers Turn:\n\n")

        coords = ge.cli_coordinates_input()
        shot = ge.attack(coords, players["ai"][0], players["ai"][1])

        #If it is a hit then "Hit" should be printed and a check needs to be made to see if the game is over
        if shot:
            print("Hit")
            #Assume the game is over
            gameOver = True
            won = True
            #If there are any ships left with a size that is not 0 then the game is not over
            for value in players["ai"][1].values():
                if value != 0:
                    gameOver = False
                    won = False
                    break
        else:
            print("Miss")

        #AI's turn
        print("\n\nAI's Turn\n\n")
        coords = generate_attack(size)
        print(f"AI guessed {coords}\n")
        shot = ge.attack(coords, players["player"][0], players["player"][1])

        for i in range(size):
            print(players["player"][0][i])

        #If it is a hit then "Hit" shouls be printed and a check needs to be made to see if the game is over
        if shot:
            print("Hit")
            #Assume the game is over
            gameOver = True
            #If there are any ships left with a size that is not 0 then the game is not over
            for value in players["player"][1].values():
                if value != 0:
                    gameOver = False
                    break
        else:
            print("Miss")
    
    if won:
        print("Congratulations, you won!")
    else:
        print("You lost.")


if __name__ == "__main__":
    ai_opponent_game_loop()




    