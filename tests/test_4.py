import pytest

from mypkg.Base_Code import BigEnemy, Enemy

# Tests for BigEnemy class


def test_initialize():
    enemy = BigEnemy(50, 50)
    assert(enemy.sizeX == 80)
    assert(enemy.sizeY == 60)


def test_update():
    enemy = BigEnemy(50, 50)
    enemy.initialize()
    enemy.update()
    assert(enemy.invincible == False)


def test_damage():
    enemy = BigEnemy(50, 50)
    enemy.initialize()
    enemy.update()
    enemy.takeDamage(2)
    assert(enemy.health == 3)
    assert(enemy.maxHealth == 5)
