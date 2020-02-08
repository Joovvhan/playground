'''An example to show how to set up an pommerman game programmatically'''
import pommerman
from pommerman import agents

print(pommerman)
print(agents)

import time
import numpy as np


def main():
    '''Simple function to bootstrap a game.
       
       Use this as an example to set up your training env.
    '''
    # Print all possible environments in the Pommerman registry
    print(pommerman.REGISTRY)

    # Create a set of agents (exactly four)
    agent_list = [
        # agents.PeaceAgent(),
        # agents.PeaceAgent(),
        # agents.PeaceAgent(),
        agents.SimpleAgent(),
        agents.SimpleAgent(),
        agents.SimpleAgent(),
        agents.MyAgent(),
        # agents.PeaceAgent(),
        # agents.SimpleAgent(),
        # agents.PlayerAgentBlocking(agent_control='wasd'),
    ]
    # Make the "Free-For-All" environment using the agent list
    env = pommerman.make('PommeFFACompetition-v0', agent_list)

    # Run the episodes just like OpenAI Gym
    for i_episode in range(1):
        state = env.reset()
        done = False
        while not done:
            env.render()
            actions = env.act(state)
            # if np.random.random() > 0.8:
            #     actions = [5] * 4
            # print('[ACTIONS: {}]'.format(actions))
            state, reward, done, info = env.step(actions)
            # input()
            # time.sleep(3)
        print('Episode {} finished'.format(i_episode))
    env.close()


if __name__ == '__main__':
    main()
