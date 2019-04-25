import pytest

from mypkg.Base_Code import Player, Wall, Enemy, screen_width, screen_height, wall_width, Level, Weapon, wall_list

# Tests for PLayer class


def test_init():
    player = Player(50, 50)
    assert(player.sizeX == 50)
    assert(player.sizeY == 50)
    assert(player.health == 10)
    assert(player.dead == False)


def test_update():
    player = Player(50, 50)
    weapon = Weapon(25, 50)
    level = Level(player, weapon)
    level.createWalls()
    player.rect.x = screen_width/2
    player.rect.y = screen_height/2
    global wall_list

    player.speedX = 1
    for i in range(5000):
        player.update()

    assert(player.rect.right == screen_width - wall_width)


def test_damage():
    player = Player(50, 50)
    player.takeDamage(2)
    assert(player.health == 8)
    assert(player.maxHealth == 10)
    assert(player.invincible == True)
