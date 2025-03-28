# Quoridor LAN Game

A Python 2 implementation of the Quoridor board game for two players over LAN. The game consists of a server that facilitates communication between the players.

Note: This project was originally developed in 2018 using Python 2, which is now deprecated. I am sharing it as-is for archival purposes. If you wish to run it, you may need to use a Python 2 environment or update it for Python 3 compatibility.

## Features
- Two-player Quoridor game over LAN.
- Server-client architecture.
- Real-time gameplay.

## Requirements
- Python 2.x
- Required libraries: pygame, socket, select

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/your-repository.git
   ```
2. Navigate to the project directory:
   ```sh
   cd your-repository
   ```
3. Run the server:
   ```sh
   python Server.py
   ```
4. Run the client for each player:
   ```sh
   python Client.py
   ```

## How to Play
- Start the server first.
- Each player should run the client script and connect to the server.
- Players take turns moving their pieces or placing walls to block their opponent.
- The goal is to reach the opposite side of the board before your opponent.
- Further instructions are inside the game itself!

## Notes
- Both players must be on the same network.
- Ensure that the correct IP and port are configured in `Client.py` to connect to the server.

## License
This project is open-source under the [MIT License](LICENSE). Feel free to modify and improve it!
