# 貓屎大戰 (Python + Pygame)

## Features
- Multi-frame sprite animation (idle, walk, attack, jump, hit, special, etc)
- Local 2P battle and single player with AI
- Combo and special move input system
- Health and energy bars
- Round system and win/lose logic
- Animated background
- Sound effects and background music

## Project Structure
```
dough/
  assets/
    sprites/
      player1/
      player2/
    backgrounds/
    sounds/
  貓屎大戰.py
  utils.py
  README.md
```

## Requirements
- Python 3.8+
- pygame (`pip install pygame`)

## How to Play
- Run `python 貓屎大戰.py`
- Player 1: WASD (move), J (attack), K (special)
- Player 2: Arrow keys (move), Num1 (attack), Num2 (special)

## Assets
- You can use your own sprite sheets (PNG) for characters and backgrounds.
- Place them in the appropriate folders under `assets/`.

## TODO
- [ ] Character animation and state machine
- [ ] Combo and special move system
- [ ] AI opponent
- [ ] Sound and music integration