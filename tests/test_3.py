import pytest

from mypkg.Base_Code import Enemy, BigEnemy

# Tests to compare Enemy class vs BigEnemy class


def test_health():
    enemy = Enemy(50, 50)
    bigEnemy = BigEnemy(50, 50)
    assert(enemy.maxHealth < bigEnemy.maxHealth)


def test_frequency():
    # enemy_list = []
    # big_enemy_list = []
    equalFrequency = False
    for i in range(1000):
        enemy = Enemy(50, 50)
        bigEnemy = BigEnemy(50, 50)
        # enemy_list.append(enemy)
        # big_enemy_list.append(bigEnemy)
        if enemy.frequency >= bigEnemy.frequency:
            equalFrequency = True

    assert(equalFrequency == False)
