# Project: Real-Time Ping Pong Game

An interactive terminal-based ping pong game developed using **Pygame**, emphasizing object-oriented design, collision mechanics, dynamic gameplay states, and immersive audio feedback.

## Overview

This project delivers a fully functional ping pong game featuring player-controlled and AI-driven paddles, responsive ball physics, score tracking, and comprehensive game state management designed for competitive play.

### **Additional Enhancements**
- Dual control scheme: supports both W/S and Arrow keys for paddle movement flexibility.
- Intelligent AI opponent with realistic tracking and deliberate reaction delays for balanced gameplay.
- Progressive difficulty: ball speed increases slightly with each paddle hit to maintain engagement.
- Visual polish with centered dashed line, large score displays, and target score indicators.

## Technology Stack

- **Python 3.10+**
- **Pygame 2.5.0+** - Graphics rendering and game loop management
- **Object-Oriented Architecture** - Modular design with separate classes for game components

## Installation & Setup

### Prerequisites
Ensure Python 3.10 or higher is installed on your system.

### Installation Steps

1. **Clone the repository:**
- **git clone - https://github.com/NipunRao05/ping-pong.git**
- **cd ping-pong**

2. **Install dependencies:**
- **pip install -r requirements.txt**

3. **Run the game:**
- **python main.py**


## Game Controls

| **Action** | **Keys** |
|------------|----------|
| Move Paddle Up | `W` or `↑ Arrow` |
| Move Paddle Down | `S` or `↓ Arrow` |
| Exit Game | `ESC` |
| Select Best of 3 | `3` (Replay Menu) |
| Select Best of 5 | `5` (Replay Menu) |
| Select Best of 7 | `7` (Replay Menu) |

## Gameplay Mechanics

### **Paddle Physics**
- Smooth movement with boundary constraints preventing paddles from leaving the screen.
- AI paddle employs intelligent tracking with position-based thresholds for natural gameplay feel.

### **Ball Dynamics**
- Random initial velocity directions ensure varied gameplay starts.
- Wall collision detection reverses vertical velocity with appropriate sound feedback.
- Paddle collision applies horizontal velocity reversal plus spin based on impact location.
- Progressive speed increase (5% per hit) maintains challenge escalation.

### **Scoring System**
- Point awarded when opponent misses the ball.
- Configurable winning thresholds through replay menu selection.
- Real-time score display positioned above respective court halves.

## Audio System

The game features three distinct sound effects:

- **paddle_hit.wav** - Triggered on successful paddle-ball collision
- **wall_bounce.wav** - Plays when ball rebounds from top/bottom walls
- **score.wav** - Activated when a point is scored

**Note:** Game operates normally without sound files, printing warnings if audio initialization fails.

## Project Architecture

ping-pong/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── paddle.py
│   └── ball.py
├── sounds/
│   ├── paddle_hit.wav
│   ├── wall_bounce.wav
│   └── score.wav
└── README.md




