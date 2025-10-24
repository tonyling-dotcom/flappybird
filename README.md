# Flappy Bird - City Edition 🐦🏙️

A modern take on the classic Flappy Bird game with a beautiful city theme, enemies to catch, and progressive difficulty levels!

## Features

✨ **Beautiful City-Themed Graphics** - Colorful buildings with windows as obstacles
🎮 **Progressive Difficulty** - 5 levels with increasing challenge
🎵 **Sound Effects & Music** - Immersive audio experience
🏆 **High Score Tracking** - Compete with yourself
👾 **Flying Enemies** - Catch enemies for bonus points
🪙 **Collectible Coins** - Floating animated gold coins to collect
💥 **Enemy Projectiles** - Dodge glowing energy balls shot by enemies
🎯 **Smooth Gameplay** - Easy controls, challenging dodging mechanics

## Installation

1. Make sure Python 3.7+ is installed
2. Activate the virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```bash
   python flappy_bird.py
   ```

2. **Controls:**
   - `SPACE` or `LEFT MOUSE CLICK` - Make the bird flap
   - Click `START` button to begin

3. **Objective:**
   - Navigate through the building gaps
   - Avoid hitting the buildings (walls)
   - **Dodge enemy projectiles** - glowing energy balls!
   - Catch flying enemies for bonus points (+3 per enemy)
   - Collect floating gold coins (+2 per coin)
   - Pass through gaps to score points (+1 per gap)
   - Survive as long as possible!

## Game Mechanics

- **Bird doesn't fall at start** - Game begins when you first flap
- **Enemies come to you** - Dark ravens fly towards the player with wave motion
- **Enemy projectiles** - Ravens shoot slow-moving energy balls that you must dodge
- **Floating coins** - Animated gold coins rotate and float across the screen
- **Generous spacing** - Buildings are well-spaced but projectiles add challenge
- **Progressive levels** - Game gets harder as you score more points

## Levels

1. **Easy Glide** (0-4 points) - Learn the basics
2. **City Cruiser** (5-9 points) - Getting faster
3. **Urban Flyer** (10-14 points) - Real challenge begins
4. **Skyline Master** (15-19 points) - For skilled players
5. **Legendary Bird** (20+ points) - Ultimate challenge!

## Customization

Edit `levels.json` to customize:
- Wall speed and spawn rate
- Enemy speed and spawn rate
- Enemy shooting frequency and projectile speed
- Coin speed and spawn rate
- Gap sizes between walls
- Score requirements for each level
- Game physics (gravity, flap strength)
- Points per collectible (walls, enemies, coins)

## Assets

All game assets are located in the `assets` folder:
- **Images**: `assets/images/` (player, enemy, background)
- **Audio**: `assets/audio/` (background music, sound effects)

## High Score

Your high score is automatically saved in `highscore.json` and persists between game sessions.

## Tips for Success

- 🎯 Wait for the right moment to flap
- 💥 Watch for glowing projectiles and dodge them!
- 🦅 Catch enemies for quick score boosts (+3 points)
- 🪙 Collect coins for extra points (+2 points)
- 🏢 Stay centered between buildings when possible
- 🎵 Play with sound on for better timing
- 🔄 Projectiles are slow - you have time to react!
- 💪 Practice makes perfect!

Enjoy the game! 🎮✨

