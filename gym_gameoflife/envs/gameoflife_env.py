import os, subprocess, time, signal
import gym
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import game

import logging
logger = logging.getLogger(__name__)

class GameOfLifeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.rows = 10
        self.columns = 10
        self.max_generations = 100
        # Create the initial random Game of Life grids
        self.current_generation = game.create_initial_grid(rows, cols)
        self.action_space = spaces.Discrete(16)
        # 8 + 8
        # 8 units in the last layer of the NN learning the first thing
        # (because a square can have max 8 numbers)
        # + 8 neurons for learning the second thing that we need to define the rules
        self.observation_space = spaces.Discrete(self.rows * self.columns)

    def __del__(self):
        self.env.act(hfo_py.QUIT)
        self.env.step()
        os.kill(self.server_process.pid, signal.SIGINT)
        if self.viewer is not None:
            os.kill(self.viewer.pid, signal.SIGKILL)


    def step(self, action): # array of 16 things
        x = max(action[0:7])
        y = max(action[8:15])

        self.status = self.env.step()
        reward = self._get_reward()
        ob = self.env.getState()
        episode_over = self.status != hfo_py.IN_GAME
        #
        # return np.array(self.state), reward, done, {}
        return ob, reward, episode_over, {}

    def _get_reward(self):
        """ Reward is given for scoring a goal. """
        if self.status == hfo_py.GOAL:
            return 1
        else:
            return 0

    def reset(self):
        """ Repeats NO-OP action until a new episode begins. """
        while self.status == hfo_py.IN_GAME:
            self.env.act(hfo_py.NOOP)
            self.status = self.env.step()
        while self.status != hfo_py.IN_GAME:
            self.env.act(hfo_py.NOOP)
            self.status = self.env.step()
        return self.env.getState()

    def render(self, mode='human', close=False):
        """ Viewer only supports human mode currently. """
        if close:
            if self.viewer is not None:
                os.kill(self.viewer.pid, signal.SIGKILL)
        else:
            if self.viewer is None:
                self._start_viewer()
