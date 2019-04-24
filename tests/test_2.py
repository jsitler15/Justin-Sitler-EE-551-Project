import pytest

from mypkg.Base_Code import Player, Weapon, Enemy, Level, wall_list

# Tests for creating levels


def test_walls():
    player = Player(50, 50)
    weapon = Weapon(20, 50)
    level = Level(player, weapon)
    level.createWalls()
    assert(len(wall_list) == 4)

def test_Enemy():
    player = Player(50, 50)
    weapon = Weapon(20, 50)
    level = Level(player, weapon)
    level.createEnemy(5)
    assert(len(level.enemy_list) == 5)

