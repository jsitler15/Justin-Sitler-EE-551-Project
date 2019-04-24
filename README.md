EE551 Python Project by Justin Sitler

Objective:
- To create a simple 2D game similar to The Legend of Zelda, in which the player can move the character, attack,
defeat enemies, and reach higher levels

Features:
- 1 player game
- Uses Pygame library to create interactive graphics
- Enemies who attack character and must be defeated with a sword attack
- Two Levels currently, but Level class has been created to easily add more
- Player class which can move using WASD inputs, and move sword using mouse tracking
- Enemy class created which forms a template to create different types of enemies
- Weapon class created which forms a template to create different types of weapons
- Walls class which the player cannot move through, which forms boundary of room (could also be obstacles within room)
- Game over screen for winning or losing, displaying cumulative score

Future improvements to the game:
- Create .png images for background, characters, enemies, etc instead of using simple rectangles and ellipses
- More types of enemies, with more interesting movement / attack patterns (for example, Boss enemy)
- Create more levels, potentially randomly created levels with unique wall layout, enemy composition, and items
- Introduce Item class and an inventory list, allowing player to use different weapons and other effects
- Background music and sound effects
- More sophisticated player / enemy attacks, animations for attacks