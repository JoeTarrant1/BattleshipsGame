from flask import Flask, render_template, request, jsonify
import components as cmp
import game_engine as ge
import mp_game_engine as mpge
import json

app = Flask(__name__)

@app.route("/placement", methods=["GET", "POST"])
def placement_interface():

    #Initialise global variables
    global playerBoard
    playerBoard = cmp.initialise_board()
    global playerShips
    playerShips = cmp.create_battleships()

    global aiBoard
    aiBoard = cmp.initialise_board()
    global aiShips
    aiShips = cmp.create_battleships()

    global size
    size = len(playerBoard[0])
    
    #When the user goes to the url the page needs to be rendered
    if request.method == "GET":
        return render_template("placement.html", ships=playerShips, board_size=size)

    #When the user presses the submit button the data sent back from the placement page should be processed
    if request.method == "POST":
        data = request.get_json()

        #This puts the returned data into the placement json so that it can be read from in the placement function
        with open("placement.json", "w") as file:
            json.dump(data, file)

        #This places the player battleships acording to the placement json
        playerBoard = cmp.place_battleships(playerBoard, playerShips, "custom")

        #This places the AI ships in random positions
        aiBoard = cmp.place_battleships(aiBoard, aiShips, "random")

        return jsonify({'message': 'Received'}), 200


@app.route("/", methods=["GET"])
def root():
    #When the user visits this url the page must be rendered
    if request.method == "GET":
        return render_template("main.html", player_board=playerBoard)

@app.route("/attack", methods=["GET"])
def process_attack():
    if request.method == "GET":
        #This gets the coordinates of the square that the user clicked on
        x = request.args.get("x")
        y = request.args.get("y")

        #Generate an AI attack
        aiAttack = mpge.generate_attack(size)

        #Process the attacks of both the player and AI
        playerShot = ge.attack((int(y), int(x)), aiBoard, aiShips)
        aiShot = ge.attack(aiAttack, playerBoard, playerShips)

        playerWin = False
        aiWin = False

        #If the player hit a ship assume the player has won
        if playerShot:
            playerWin = True

            #Check through all the AI ships to see if there are any left, if so the game should continue
            for value in aiShips.values():
                if value != 0:
                    playerWin = False
                    break
        
        #If the player has won, return relevent details to the page
        if playerWin:
            return jsonify({"hit":playerShot, "AI_Turn":aiAttack, "finished":"Game Over, Player Wins"})
            
        #If AI hits a ship assume the AI has won
        if aiShot:
            aiWin = True

            #Check through all the player ships to see if there are any left, if so the game should continue
            for value in playerShips.values():
                if value != 0:
                    aiWin = False
                    break

        #If the AI has won then return the relevent details to the page
        if aiWin:
            return jsonify({"hit":playerShot, "AI_Turn":aiAttack, "finished":"Game Over, AI Wins"})
        
        #If neither the player or the AI won then return the relevent details to the page
        if not playerWin and not aiWin:
            return jsonify({"hit":playerShot, "AI_Turn":aiAttack})

if __name__ == "__main__":
    app.run()