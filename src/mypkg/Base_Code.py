# Justin Sitler EE-551 Project:
# Creating a single player game to defeat enemies, using Pygame

# Import the required libraries
import sys
import pygame
import math
import random

# For reproducibility, use a set random seed so the enemies will always be created the same
random.seed(1)

# Game parameters
wall_width = 10
screen_width, screen_height = 1000, 700

# Inititalize Pygame, create the screen and the game clock
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Sprite Groups act like object arrays for sprites with ability to call functions like update() for every object in the group
all_sprites_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()


# Function to easily display text. Optional Size and Color inputs
def message_display(text, posX, posY, size=20, color=(0,0,0)):
    largeText = pygame.font.Font('freesansbold.ttf', size)

    TextSurf = largeText.render(text, True, color)
    TextRect = TextSurf.get_rect()
    TextRect.center = (posX, posY)
    screen.blit(TextSurf, TextRect)


# Function to display Game Over screen when you lose
def gameOver(score):
    done = False
    while not done:
        screen.fill((0, 0, 0))
        message_display("Game Over!", screen_width/2, screen_height/2, 80, color=(255, 0, 0))
        message_display("Score: " + str(score), screen_width / 2, 400, color=(255, 0, 0))
        message_display("Press ENTER to Exit", screen_width/2, 500, color=(255, 0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True


# Function to display Congratulations screen when you win
def gameWon(score):
    done = False
    while not done:
        screen.fill((255, 255, 0))
        message_display("Congratulations!", screen_width/2, screen_height/2, size=80, color=(0, 255, 0))
        message_display("Score: " + str(score), screen_width/2, 400, color=(0, 255, 0))
        message_display("Press ENTER to Exit", screen_width/2, 500, color=(0, 255, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True


# Creates a class Player, which inherits properties from Pygame's Sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        # Important parameters include size, position, color, health points, and status of alive/dead
        self.sizeX = width
        self.sizeY = height
        self.color = (0, 255, 0)
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        self.speedX = 0
        self.speedY = 0
        self.score = 0
        self.dead = False
        self.maxHealth = 10
        self.health = self.maxHealth
        self.rect = self.image.get_rect()
        self.center = self.rect.center
        self.invincible = False
        self.startinvul = 0

    # Moves the player based on speed (speed is modified by Level.update() function)
    def update(self):
        global wall_list
        self.center = self.rect.center

        # Attempts to move right / left, but checks for collision with walls to override this if necessary
        self.rect.x += self.speedX
        wall_hit_list = pygame.sprite.spritecollide(self, wall_list, False)
        for walls in wall_hit_list:
            if self.speedX > 0:
                self.rect.right = walls.rect.left
            else:
                self.rect.left = walls.rect.right

        # Attempts to move up / down, but checks for collision with walls to override this if necessary
        self.rect.y += self.speedY
        wall_hit_list = pygame.sprite.spritecollide(self, wall_list, False)
        for walls in wall_hit_list:
            if self.speedY > 0:
                self.rect.bottom = walls.rect.top
            else:
                self.rect.top = walls.rect.bottom

        # If the player is invincible (happens when Player takes damage), turn red to indicate this
        if self.invincible:
            self.image.fill((255, 0, 0))
        else:
            self.image.fill(self.color)

        # Checks to see for how long the player should be invincible for
        currenttime = pygame.time.get_ticks()
        if currenttime - self.startinvul >= 1000:
            self.invincible = 0

    # If the player takes damage, decreases health and starts the timer for invincibility
    def takeDamage(self, amount):
        self.health -= amount
        self.startinvul = pygame.time.get_ticks()
        self.invincible = True


# Weapon class, inherits from Sprite class
class Weapon(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        # Important parameters include color, size, position, ellipse image, and damage dealt by weapon
        self.color = (100, 100, 100)
        self.sizeX = width
        self.sizeY = height
        self.originalIimage = pygame.Surface([width, height])
        self.originalIimage.fill((255, 255, 255))
        self.originalIimage.set_colorkey((255, 255, 255))
        self.image = self.originalIimage
        pygame.draw.ellipse(self.image, self.color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.center = [self.rect.x + self.sizeX/2, self.rect.y + self.sizeY/2]
        self.damageDealt = 1

    # Updates position to point to the mouse position
    def update(self, player):
        global mouseX, mouseY
        playerPosX = player.center[0]
        playerPosY = player.center[1]
        playerSizeX = player.sizeX
        playerSizeY = player.sizeY
        vector = math.atan2((mouseY - playerPosY), (mouseX - playerPosX))
        self.image = pygame.transform.rotate(self.originalIimage, -math.degrees(vector)+90)
        posX = playerPosX + playerSizeX*math.cos(vector)*1.2
        posY = playerPosY + playerSizeY*math.sin(vector)*1.2
        self.rect = self.image.get_rect(center=(posX, posY))


# Creates an regular Enemy class which inherits functions from Player class.
class Enemy(Player):
    def __init__(self, startPosX, startPosY):
        pygame.sprite.Sprite.__init__(self)

        # Important parameters include size, position, color, max health, score for damaging/killing, and damage dealt
        # These vary among different enemy types
        self.sizeX = 25
        self.sizeY = 15
        self.color = (0, 0, 255)
        self.damageDealt = 1
        self.maxHealth = 3
        self.frequency = random.randrange(100, 500)
        self.startPosX = startPosX
        self.startPosY = startPosY
        self.hitScore = 5
        self.killScore = 50

    # When created, Enemy trajectory must be initialized. It will have a random starting point, and oscillate
    # around this point with a random trajectory (major/minor axis of ellipse), frequency (speed), and direction
    # (clockwise vs counterclockwise). This is the same for every enemy type
    def initialize(self):
        self.image = pygame.Surface([self.sizeX, self.sizeY])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.startPosX, self.startPosY)
        self.health = self.maxHealth
        self.rect.center = (self.startPosX, self.startPosY)
        minX = int(min(screen_width - wall_width - (self.startPosX + self.sizeX/2),
                   (self.startPosX - self.sizeX/2) - wall_width))
        minY = int(min(screen_height - wall_width - (self.startPosY + self.sizeY/2),
                   (self.startPosY - self.sizeY/2) - wall_width))
        trajectoryX = random.randrange(0, minX)
        trajectoryY = random.randrange(0, minY)
        self.direction = random.choice((-1, 1))
        self.traj = [trajectoryX, trajectoryY, self.frequency]
        self.center = [self.rect.x + self.sizeX/2, self.rect.y + self.sizeY/2]
        self.invincible = False
        self.startinvul = 0

    # Update self to check invincibility and move the object along its trajectory
    def update(self):
        if self.invincible:
            self.image.fill((255, 0, 0))
        else:
            self.image.fill(self.color)

        currenttime = pygame.time.get_ticks()
        if currenttime - self.startinvul >= 1000:
            self.invincible = 0

        self.rect.x = self.startPosX + (-math.cos(self.direction*currenttime/self.traj[2])*self.traj[0])
        self.rect.y = self.startPosY + (-math.sin(self.direction*currenttime/self.traj[2])*self.traj[1])


# Creates a BigEnemy class which inherits functions from regular Enemy. This lets more types of enemies be created
# in future additions to the game (right now there is only two)
class BigEnemy(Enemy):
    def __init__(self, startPosX, startPosY):
        pygame.sprite.Sprite.__init__(self)

        # BigEnemy is larger, meaning it has more health, deals more damage, is slower, and is worth more points
        self.sizeX = 80
        self.sizeY = 60
        self.color = (0, 0, 0)
        self.damageDealt = 2
        self.maxHealth = 5
        self.frequency = random.randrange(600, 800)
        self.startPosX = startPosX
        self.startPosY = startPosY
        self.hitScore = 5
        self.killScore = 100


# the Wall class inherits from the Sprite group, and is simply an object that the player cannot move through
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


# a Level class initializes the game by creating Walls, enemies, and checking for interactions between the player
# and the enemies. It also contains the indefinite loop for running the game
class Level(object):
    def __init__(self, player, weapon):
        # Each level checks for interactions with the player and the weapon, and creates its own list of enemies
        self.player = player
        self.weapon = weapon
        self.enemy_list = pygame.sprite.Group()
        self.big_enemy_list = pygame.sprite.Group()

    # Creates the background walls for a given level. This could be modified in other Level classes to create
    # different terrain.
    def createWalls(self):
        wall = Wall(0, 0, wall_width, screen_height)
        wall_list.add(wall)
        all_sprites_list.add(wall)

        wall = Wall(wall_width, 0, screen_width - wall_width * 2, wall_width)
        wall_list.add(wall)
        all_sprites_list.add(wall)

        wall = Wall(screen_width - wall_width, 0, wall_width, screen_height)
        wall_list.add(wall)
        all_sprites_list.add(wall)

        wall = Wall(wall_width, screen_height - wall_width, screen_width - wall_width * 2, wall_width)
        wall_list.add(wall)
        all_sprites_list.add(wall)

    # Creates a given amount of regular enemies for the level at random positions, initializes them, and then adds the
    # sprites to the appropriate groups.
    def createEnemy(self, quantity):
        for i in range(quantity):
            enemy = Enemy(random.randrange(int(screen_width / 3), int(screen_width * 2 / 3)),
                          random.randrange(int(screen_height / 3), int(screen_height * 2 / 3)))
            enemy.initialize()
            self.enemy_list.add(enemy)
            all_sprites_list.add(enemy)

    # Creates a given amount of Big enemies similar to the previous function
    def createBigEnemy(self, quantity):
        for i in range(quantity):
            bigenemy = BigEnemy(random.randrange(int(screen_width / 3), int(screen_width * 2 / 3)),
                                random.randrange(int(screen_height / 3), int(screen_height * 2 / 3)))
            bigenemy.initialize()
            self.enemy_list.add(bigenemy)
            all_sprites_list.add(bigenemy)

    # Update function has a few important tasks including checking collisions
    def update(self):
        # Updates the weapon's position
        self.weapon.update(self.player)

        # Checks for collision between all enemies and the weapon
        enemy_hit_list = pygame.sprite.spritecollide(self.weapon, self.enemy_list, False)

        # Each enemy hit takes damage if it is not invincible, and removes it from the sprite Group if its health is
        # zero (using the kill() function). Increases player score on hit / kill
        for enemy in enemy_hit_list:
            if not enemy.invincible:
                enemy.takeDamage(self.weapon.damageDealt)
                if enemy.health <= 0:
                    self.player.score += enemy.killScore
                    enemy.kill()
                else:
                    self.player.score += enemy.hitScore

        # Checks for collision between all enemies and the player
        player_hit = pygame.sprite.spritecollide(self.player, self.enemy_list, False)

        # If the player is hit, it takes damage and reduces score
        for enemy in player_hit:
            if not self.player.invincible:
                self.player.takeDamage(enemy.damageDealt)
                self.player.score -= 5

        # Moves the player and the enemies according to their respective update() functions
        self.enemy_list.update()
        self.player.update()

        # Draws all sprites on the screen
        all_sprites_list.draw(screen)

        # Sets the game frame rate
        clock.tick(500)

        # Updates the screen
        pygame.display.flip()

    # Loop function which contains the indefinite loop and the previously written update() function
    def loop(self):
        global mouseX, mouseY
        done = False

        # Repeating loop until conditons are met (done)
        while not done:
            # White background
            screen.fill((255, 255, 255))

            # Display player health and score
            message_display(("Health: " + str(self.player.health)), screen_width - 100, 50)
            message_display(("Score: " + str(self.player.score)), screen_width - 100, 150)

            # Pygame event queue, which allows events such as key strokes, mouse movement, and others to be input
            # simultaneously then carried out in a set order
            for event in pygame.event.get():  # If the player closes the window:
                if event.type == pygame.QUIT:
                    done = True
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:  # Tracks mouse motion
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                elif event.type == pygame.KEYDOWN:  # Player uses WASD to move, pressing button changes speed
                    if event.key == pygame.K_w: self.player.speedY -= 1
                    if event.key == pygame.K_d: self.player.speedX += 1
                    if event.key == pygame.K_s: self.player.speedY += 1
                    if event.key == pygame.K_a: self.player.speedX -= 1
                elif event.type == pygame.KEYUP:  # Releasing changes speed so you only move when key is pressed
                    if event.key == pygame.K_w: self.player.speedY += 1
                    if event.key == pygame.K_d: self.player.speedX -= 1
                    if event.key == pygame.K_s: self.player.speedY -= 1
                    if event.key == pygame.K_a: self.player.speedX += 1

            # Calls the previously written update function
            self.update()

            # Quits the loop if all enemies have been killed
            if len(self.enemy_list) == 0:
                done = True

            # Quits the loop and ends game if the player health reaches zero
            if self.player.health <= 0:
                done = True
                self.player.dead = True
                gameOver(self.player.score)


# Main function to carry out the desired functions
def main():
    # Create "player" object
    player = Player(50, 50)
    player.rect.x = screen_width / 2 - player.sizeX / 2
    player.rect.bottom = screen_height - wall_width
    player.walls = wall_list

    # Create "sword" object
    sword = Weapon(20, 50)
    sword.rect.x = player.rect.x
    sword.rect.y = player.rect.y

    # Add sprites to array of all sprites
    all_sprites_list.add(player)
    all_sprites_list.add(sword)

    # Create easy Level 1, with 5 regular enemies
    level1 = Level(player, sword)
    level1.createWalls()
    level1.createEnemy(5)
    level1.loop()

    # Checks if player has died to see whether to continue:
    if not player.dead:
        # Creates harder Level 2 with 3 Big enemies
        level2 = Level(player, sword)
        level2.createBigEnemy(3)
        level2.loop()

    # If the player survives the two levels, display win screen. More levels could be added in future
    if not player.dead:
        gameWon(player.score)

    # Exits Pygame
    pygame.quit()


main()

