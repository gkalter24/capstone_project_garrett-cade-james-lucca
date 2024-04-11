from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# A simplified game state
game_state = {
    'players': {},  # Track players e.g., {'player_id': {'x': 100, 'y': 100, 'size': 20}}
    'food': []  # List of food positions and sizes
}

def update_game_state():
    # Placeholder for your game logic
    # Here you would update player positions, check for collisions, etc.
    pass

def broadcast_game_state():
    # Broadcasts the current game state to all connected clients
    socketio.emit('game_state', game_state)

@app.route('/')
def index():
    # Serve the game's frontend
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # Initialize player state, etc.

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    # Clean up player state

@socketio.on('move')
def handle_move(data):
    print(f"Move: {data}")
    # Update player state based on move
    # This is where you'd adjust the player's position in the game state

def game_loop():
    """Runs the main game loop."""
    while True:
        update_game_state()
        broadcast_game_state()
        time.sleep(0.016)  # Approx. 60 FPS

if __name__ == '__main__':
    # Start the game loop in a separate thread
    thread = Thread(target=game_loop)
    thread.start()
    # Start the Flask application
    socketio.run(app, debug=True)
