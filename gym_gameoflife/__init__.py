import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='GameOfLife-v0',
    entry_point='gym_gameoflife.envs:GameOfLifeEnv',
    timestep_limit=1000,
    reward_threshold=1.0,
    nondeterministic = True,
)
