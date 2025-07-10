# 🎮 Real-Time Tic-Tac-Toe Game

A modern, browser-based Tic-Tac-Toe game built with FastAPI and WebSockets, enabling real-time multiplayer gameplay between two players.

## 🌟 Features

- **Real-time multiplayer gameplay** using WebSocket connections
- **Automatic player assignment** - first player gets X, second gets O
- **Live game state updates** - board updates instantly after each move
- **Smart game logic** - automatic win detection and draw handling
- **Modern web interface** with responsive design
- **Concurrent game sessions** support

## 🚀 Demo

*Main game interface showing the interactive board*

![Game Interface](https://github.com/user-attachments/assets/42bafa36-cb2c-4179-a3cf-4c03909425b5)

*Real-time gameplay between two players*

![Gameplay](https://github.com/user-attachments/assets/15023374-4115-472f-8fdc-b3d8598dab86)

*Win detection and game completion*

![Game Results: Win](https://github.com/user-attachments/assets/e3c18f9d-e17a-4ebe-bf57-017e298e08a4)
![Game Results: Draw](https://github.com/user-attachments/assets/c06fd275-49c1-4e58-9b54-07bb176a03ff)


## 🛠 Tech Stack

- **Backend**: FastAPI (Python)
- **Real-time Communication**: WebSockets
- **Frontend**: HTML/CSS/JavaScript
- **Architecture**: Asynchronous server-client communication

## 📋 Prerequisites

- Python 3.7+
- pip (Python package manager)

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/AntoninaDavidenko/TicTacToe.git
   cd TicTacToe
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn websockets
   ```

4. **Run the server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Open your browser**
   Navigate to `http://localhost:8000` to start playing!

## 🎯 How to Play

1. **Start the game**: Open the application in your browser
2. **Wait for opponent**: The game requires two players to begin
3. **Make your move**: Click on any empty cell to place your mark
4. **Win condition**: Get three marks in a row (horizontally, vertically, or diagonally)
5. **New game**: Refresh the page to start a new game

## 🏗 Project Structure

```
TicTacToe/
├── main.py              # FastAPI server and WebSocket endpoints
├── static/
│   ├── index.html       # Game interface
│   ├── style.css        # Styling
│   └── script.js        # Client-side game logic
└── README.md           # Project documentation
```

## 🔌 API Endpoints

### WebSocket Endpoints

- `WS /ws/{client_id}` - Establishes WebSocket connection for real-time game communication

### HTTP Endpoints

- `GET /` - Serves the main game interface
- `GET /static/{filename}` - Serves static files (CSS, JS, images)

## 🎮 Game Flow

1. **Connection**: Two players connect via WebSocket
2. **Assignment**: First player automatically assigned 'X', second gets 'O'
3. **Turn Management**: Players alternate turns starting with 'X'
4. **Move Validation**: Server validates moves and updates game state
5. **Win Detection**: Server checks for winning combinations after each move
6. **Game End**: Game ends on win or draw, players notified via WebSocket

## 🚀 Features in Detail

### Real-time Communication
- Uses WebSocket protocol for instant communication
- Bidirectional data flow between client and server
- Real-time board state synchronization

### Game Logic
- Automatic turn management
- Win condition detection (rows, columns, diagonals)
- Draw detection when board is full
- Input validation and error handling

### User Experience
- Clean, intuitive interface
- Responsive design for different screen sizes
- Visual feedback for moves and game states
- Clear indication of current player

## 🔧 Configuration

The server can be configured with different parameters:

```bash
# Change port
uvicorn main:app --port 3000

# Enable debug mode
uvicorn main:app --reload --log-level debug

# Bind to specific host
uvicorn main:app --host 127.0.0.1
```




