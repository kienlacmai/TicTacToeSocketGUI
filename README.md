# Networked Tic-Tac-Toe with GUI

## Overview
The **Tic-Tac-Toe Socket GUI** project implements a two-player **networked Tic-Tac-Toe** game using **Python sockets** and a graphical user interface.  
The system allows two users to play against each other in real time across different computers connected to the same network or through local hosting.  

The project demonstrates fundamental concepts in **socket programming**, **client–server architecture**, and **event-driven GUI design**, integrating networking and interface development into a single cohesive application.

---

## Objectives
This project was developed to explore:
- The use of **Python’s socket library** for establishing reliable communication between distributed clients.
- The design of a responsive, interactive **graphical user interface** for real-time gameplay.
- Synchronization of game states and user inputs across two networked machines.
- Handling concurrent events, user turns, and message transmission over TCP connections.

---

## System Architecture
The application follows a **client–server architecture**, where:
- One player hosts the server, listening for incoming connections.
- The second player connects as a client using the host machine’s IP address.
- Both programs maintain synchronized game boards by exchanging state updates over socket communication.

The game runs over **TCP** to ensure reliable message delivery between nodes, preserving the integrity of each player’s moves.

---

## Functionality
Key features include:

- **Two-Player Networked Gameplay**  
  Two instances of the application connect over a local network (LAN), allowing real-time multiplayer Tic-Tac-Toe.

- **Graphical Interface**  
  The GUI provides a simple, intuitive interface for making moves, displaying turns, and announcing game results.

- **Turn Synchronization**  
  Game logic enforces valid turns and automatically updates the opponent’s board to maintain consistency.

- **Connection Feedback**  
  Players receive clear indications when connections are established or terminated.

- **Game End Detection**  
  The program identifies winning, losing, and draw states, then resets or terminates the session accordingly.

---

## Technical Implementation
- **Language:** Python  
- **Libraries:**  
  - `socket` — handles TCP communication between client and server.  
  - `threading` — allows the GUI to remain responsive while listening for network updates.  
  - `tkinter` — provides the user interface and event-driven game board.  

- **Modules:**  
  - `server.py` — initializes the hosting socket and waits for incoming connections.  
  - `client.py` — connects to a host machine and communicates move data.  
  - `gui.py` — manages visual board updates and player interactions.  
  - `game_logic.py` — tracks board states, move validation, and win conditions.

- **Network Behavior:**  
  - The host binds to a local IP address and port (commonly 127.0.0.1 or LAN IP).  
  - The client connects using the host’s IP.  
  - Messages are sent as serialized text data representing moves (e.g., cell positions).  
  - Both ends interpret incoming data to update their respective GUIs.

---
