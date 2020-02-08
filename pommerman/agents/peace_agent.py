'''An agent that preforms a random action each step'''
from . import BaseAgent
import numpy as np

passable_objects = (0, 5, 6, 7, 8)

agent_actions = list(range(5))

'''
0: 가만히
1: 위
2: 아래
3: 왼쪽
4: 오른쪽
5: 폭탄
'''


class PeaceAgent(BaseAgent):
    """The Random Agent that returns random actions given an action_space."""

    def act(self, obs, action_space):

        my_position = tuple(obs['position'])  # (y, x)
        board = np.array(obs['board'])  # (y, x)
        # action_votes = np.array([1, 1, 1, 1, 1])
        action_votes = np.array([1, 1, 1, 1, 1])

        # print(action_space)
        # return action_space.sample()
        # print('########')
        # print(obs)
        # print('########')

        action_votes = vacancy_filter(action_votes, board, my_position)

        # print('[My Position {}]: [{}]'.format(my_position, action_votes))

        action_probabilities = action_votes / np.sum(action_votes)

        return np.random.choice(agent_actions, p=action_probabilities)


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
