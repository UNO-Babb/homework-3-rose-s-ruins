from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Initialize game state
game_state = {
    "players": {
        "1": {"position": 0, "color": "red"},
        "2": {"position": 0, "color": "blue"}
    },
    "current_turn": 1,
    "log": []
}

# Save the game state to a file
def save_game_state():
    with open("game_state.txt", "w") as f:
        json.dump(game_state, f)

# Load the game state from a file
def load_game_state():
    global game_state
    try:
        with open("game_state.txt", "r") as f:
            game_state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Initialize default game state if the file is missing or corrupted
        game_state = {
            "players": {
                "1": {"position": 0, "color": "red"},
                "2": {"position": 0, "color": "blue"}
            },
            "current_turn": 1,
            "log": []
        }
        save_game_state()  # Save the default state

# Simulate rolling two dice
def roll_dice():
    from random import randint
    return randint(1, 6), randint(1, 6)

# Route to render the game interface
@app.route('/')
def index():
    return render_template('index.html')  # Renders the HTML game interface

@app.route('/roll_dice', methods=['POST'])
def handle_roll():
    global game_state
    print(f"Game state before roll: {game_state}")  # Debugging

    player = game_state["current_turn"]
    print(f"Current player: {player}")  # Debugging

    roll = roll_dice()
    print(f"Dice rolled: {roll}")  # Debugging

    move = 0

    # Movement logic based on the dice roll
    if roll[0] == roll[1]:  # Doubles
        if roll == (1, 1):  # Snake eyes
            move = -1
        else:
            move = 1

    # Update the player's position
    game_state["players"][str(player)]["position"] += move
    game_state["players"][str(player)]["position"] = max(0, game_state["players"][str(player)]["position"])
    print(f"Player {player} moves to position {game_state['players'][str(player)]['position']}")  # Debugging

    # Log the turn
    log_entry = f"Player {player} rolled {roll[0]} and {roll[1]}, moved {move} spots."
    game_state["log"].append(log_entry)
    print(f"Log entry: {log_entry}")  # Debugging

    with open("events.txt", "a") as f:
        f.write(log_entry + "\n")

    # Save the updated game state
    save_game_state()

    # Prepare the response
    response = {
        "roll": roll,
        "move": move,
        "position": game_state["players"][str(player)]["position"],
        "log": log_entry
    }

    # Switch to the next player
    game_state["current_turn"] = 2 if player == 1 else 1
    print(f"Next player: {game_state['current_turn']}")  # Debugging

    return jsonify(response)

# Initialize game state when starting the server
if __name__ == "__main__":
    load_game_state()
    app.run(debug=True)
