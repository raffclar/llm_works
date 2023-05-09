from enum import Enum
from math import floor

PROBLEM_SIZE = 1
FORK_COUNT = 5
PHILOSOPHER_COUNT = floor(5 * PROBLEM_SIZE)
STATE_TIME = 0.05


class PhilosopherState(Enum):
    THINKING = 0
    HUNGRY = 1
    EATING = 2
