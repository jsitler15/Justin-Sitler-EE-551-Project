import pytest

from mypkg.Base_Code import Enemy

# Tests for Enemy class


def test_initialize():
    enemy = Enemy(50, 50)
    assert(enemy.sizeX == 25)
    assert(enemy.sizeY == 15)


def test_update():
    enemy = Enemy(50, 50)
    enemy.initialize()
    enemy.update()
    assert(enemy.invincible == False)

def test_damage():
    enemy = Enemy(50, 50)
    enemy.initialize()
    enemy.update()
    enemy.takeDamage(2)
    assert(enemy.health == 1)
    assert(enemy.maxHealth == 3)
