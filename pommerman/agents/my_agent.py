'''An agent that preforms a random action each step'''
from . import BaseAgent
from .. import constants

import numpy as np

import matplotlib.pyplot as plt

passable_objects = (0, 5, 6, 7, 8)

agent_actions = list(range(6))

'''
0: 가만히
1: 위
2: 아래
3: 왼쪽
4: 오른쪽
5: 폭탄
'''


class MyAgent(BaseAgent):
    """The Random Agent that returns random actions given an action_space."""

    def init(self):

        plt.figure()
        dummy_array = np.random.random([11, 11])
        plt.imshow(dummy_array)
        plt.show()

    def act(self, obs, action_space):

        # agent_action = []  # list(range(6))
        action_votes = np.array([1, 1, 1, 1, 1, 0], dtype=int)

        # print(obs.keys())
        my_position = tuple(obs['position'])  # (y, x)
        board = np.array(obs['board'])  # (y, x)
        ammo = int(obs['ammo'])

        # print(board)
        # print('[Self Verification: {}]'.format(board[my_position[0]][my_position[1]]))

        enemies = [constants.Item(e) for e in obs['enemies']]

        action_votes += mine_item(my_position, board, ammo)

        action_votes += get_nearest_item(my_position, board)

        action_votes += find_bomb(my_position, board)

        action_votes = vacancy_filter(action_votes, board, my_position)

        action_votes = no_bomb_filter(action_votes, ammo)

        action_votes = danger_filter(action_votes, board, my_position)

        print('[STAY: {}] [UP: {}] [DOWN: {}] [LEFT: {}] [RIGHT: {}] [BOMB: {}]'.format(
            action_votes[0], action_votes[1], action_votes[2], action_votes[3], action_votes[4], action_votes[5]))

        if np.sum(action_votes) > 0:
            action_probabilities = action_votes / np.sum(action_votes)
        else:
            action_probabilities = np.ones(6) / 6

        print('[PROB: ({})]'.format(action_probabilities))

        return np.random.choice(agent_actions, p=action_probabilities)


def find_nearest_wooden_wall(board, pos):

    iterator = tornado_iterator()

    for position in iterator:
        a, b = position

        try:
            x = pos[1] + a
            y = pos[0] + b
            # print('[(x: {}, y: {})] => [{}]'.format(x, y, board[y, x]))
            if board[y, x] == 2:  # Rigid wall is 1 not 2, Wooden wall is number 1
                return y, x
        except IndexError:
            pass

    return -1, -1


def find_nearest_object(board, pos, objs):

    iterator = tornado_iterator()

    for position in iterator:
        a, b = position

        try:
            x = pos[1] + a
            y = pos[0] + b
            # print('[(x: {}, y: {})] => [{}]'.format(x, y, board[y, x]))
            if board[y, x] in objs:
                return y, x
        except IndexError:
            pass

    return -1, -1


def tornado_iterator():
    for i in range(1, 11):
        a = 0
        b = -i

        for j in range(1, i + 1):
            a = a + 1
            b = b + 1
            yield a, b

        for j in range(1, i + 1):
            a = a - 1
            b = b + 1
            yield a, b

        for j in range(1, i + 1):
            a = a - 1
            b = b - 1
            yield a, b

        for j in range(1, i + 1):
            a = a + 1
            b = b - 1
            yield a, b


def is_adjacent(position, x, y):
    if np.abs(position[0] - y) + np.abs(position[1] - x) <= 1:
        # print('[Wooden Wall @ ({}, {}) => Place Bomb!]'.format(x, y))
        return True
    else:
        return False


def find_bomb(position, board):

    action_votes = np.array([0, 0, 0, 0, 0, 0], dtype=int)

    try:
        if board[position[0] + 1, position[1]] == 3:
            action_votes[1] += 5
            action_votes[2] -= -5
    except IndexError:
        pass

    try:
        if board[position[0] - 1, position[1]] == 3:
            action_votes[2] += 5
            action_votes[1] -= 5
    except IndexError:
        pass

    try:
        if board[position[0], position[1] + 1] == 3:
            action_votes[3] += 5
            action_votes[4] -= 5
    except IndexError:
        pass

    try:
        if board[position[0], position[1] - 1] == 3:
            action_votes[4] += 5
            action_votes[3] -= 5
    except IndexError:
        pass

    return action_votes


def action_filter(position, board):

    # 1, 2, 3, 4 Don't try to get through a wall, bomb or flame

    return


def vacancy_filter(action_votes, board, position):

    try:
        if board[position[0] - 1, position[1]] not in passable_objects:
            action_votes[1] = 0
    except IndexError:
        action_votes[1] = 0

    try:
        if board[position[0] + 1, position[1]] not in passable_objects:
            action_votes[2] = 0
    except IndexError:
        action_votes[2] = 0

    try:
        if board[position[0], position[1] - 1] not in passable_objects:
            action_votes[3] = 0
    except IndexError:
        action_votes[3] = 0

    try:
        if board[position[0], position[1] + 1] not in passable_objects:
            action_votes[4] = 0
    except IndexError:
        action_votes[4] = 0

    return action_votes


def danger_filter(action_votes, board, position):

    danger_range = 1  # 2 has a problem

    query_position = [position[0], position[1]]
    if check_danger(board, query_position, danger_range):
        action_votes[0] = 0

    query_position = [position[0] - 1, position[1]]
    if check_danger(board, query_position, danger_range):
        action_votes[1] = 0

    query_position = [position[0] + 1, position[1]]
    if check_danger(board, query_position, danger_range):
        action_votes[2] = 0

    query_position = [position[0], position[1] - 1]
    if check_danger(board, query_position, danger_range):
        action_votes[3] = 0

    query_position = [position[0], position[1] + 1]
    if check_danger(board, query_position, danger_range):
        action_votes[4] = 0

    return action_votes


def check_danger(board, position, range_len):

    danger_count = 0

    for i in range(1, range_len + 1):
        try:
            val = board[position[0] - i, position[1]]
            if val == 0:
                pass
            elif val == 3:
                danger_count += 1
            elif val in (1, 2):
                break
        except IndexError:
            pass

    for i in range(1, range_len + 1):
        try:
            val = board[position[0] + i, position[1]]
            if val == 0:
                pass
            elif val == 3:
                danger_count += 1
            elif val in (1, 2):
                break
        except IndexError:
            pass

    for i in range(1, range_len + 1):
        try:
            val = board[position[0], position[1] - i]
            if val == 0:
                pass
            elif val == 3:
                danger_count += 1
            elif val in (1, 2):
                break
        except IndexError:
            pass

    for i in range(1, range_len + 1):
        try:
            val = board[position[0], position[1] + i]
            if val == 0:
                pass
            elif val == 3:
                danger_count += 1
            elif val in (1, 2):
                break
        except IndexError:
            pass

    return danger_count > 0


def no_bomb_filter(action_votes, ammo):

    if ammo <= 0:
        action_votes[5] = 0

    return action_votes


def mine_item(my_position, board, ammo):

    action_votes = np.array([0, 0, 0, 0, 0, 0], dtype=int)

    y, x = find_nearest_wooden_wall(board, my_position)

    # print(is_adjacent(my_position, x, y))
    # print('[(X, Y): ({}, {}) / (x, y): ({}, {})]'.format(my_position[1], my_position[0], x, y))

    if x == -1 and y == -1:
        return action_votes

    if is_adjacent(my_position, x, y):
        # agent_action.append(5)
        action_votes[5] += 5
    elif ammo > 0:
        if x - my_position[1] < 0:
            # agent_action.append(3)
            action_votes[3] += 1
        elif x - my_position[1] > 0:
            # agent_action.append(4)
            action_votes[4] += 1

        if y - my_position[0] < 0:
            # agent_action.append(1)
            action_votes[1] += 1
        elif y - my_position[0] > 0:
            # agent_action.append(2)
            action_votes[2] += 1

    return action_votes


def get_nearest_item(my_position, board):

    action_votes = np.array([0, 0, 0, 0, 0, 0], dtype=int)

    y, x = find_nearest_object(board, my_position, [6, 7, 8])

    if x == -1 and y == -1:
        return action_votes

    if x - my_position[1] < 0:
        action_votes[3] += 3
    elif x - my_position[1] > 0:
        action_votes[4] += 3

    if y - my_position[0] < 0:
        action_votes[1] += 3
    elif y - my_position[0] > 0:
        action_votes[2] += 3

    return action_votes