import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from threading import Thread, BoundedSemaphore

from concurrent_django.exercises.dining_philosophers.deadlock import PhilosopherState, STATE_TIME, FORK_COUNT, \
    PHILOSOPHER_COUNT

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


@dataclass
class Fork:
    ident: int
    name: str


class Arbitrator(BoundedSemaphore):
    def talk(self, name: str):
        _logger.info(f"Arbitrating with {name}")
        return self


class Philosopher(Thread):
    def __init__(self, run_for: int, index: int, name: str, arbitrator: Arbitrator, left: Fork, right: Fork):
        super().__init__()
        self.run_for = run_for
        self.state = PhilosopherState.THINKING
        self.index = index
        self.name = name
        self.arbitrator = arbitrator
        self.left = left
        self.right = right

    def run(self):
        time_now = datetime.now()
        end_time = time_now + timedelta(seconds=self.run_for)
        while time_now < end_time:
            self.state = PhilosopherState.THINKING
            _logger.info(f"{self.name} is thinking")
            time.sleep(STATE_TIME)
            self.state = PhilosopherState.HUNGRY
            _logger.info(f"{self.name} is hungry")
            with self.arbitrator.talk(self.name):
                self.state = PhilosopherState.EATING
                _logger.info(f"{self.name} is eating with {self.left.name} and {self.right.name}")
                time.sleep(STATE_TIME)
            time_now = datetime.now()


def start(run_for: int = None):
    philosophers = []
    forks = []
    arbitrator = Arbitrator()
    for i in range(FORK_COUNT):
        forks.append(Fork(i, f"Fork #{i + 1}"))
    for i in range(PHILOSOPHER_COUNT):
        philosophers.append(
            Philosopher(
                run_for,
                i,
                f"Philosopher #{i + 1}",
                arbitrator,
                forks[i % FORK_COUNT],
                forks[(i + 1) % FORK_COUNT]
            )
        )
    for i in range(PHILOSOPHER_COUNT):
        philosophers[i].start()
    for i in range(PHILOSOPHER_COUNT):
        philosophers[i].join()


if __name__ == "__main__":
    logging.basicConfig()
    start()
