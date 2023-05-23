import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from threading import Thread, BoundedSemaphore

from concurrent_django.exercises.dining_philosophers.shared import (
    STATE_TIME,
    PHILOSOPHER_COUNT,
    FORK_COUNT,
    PhilosopherState,
)

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


@dataclass
class LockedFork:
    ident: int
    name: str
    semaphore: BoundedSemaphore


class DeadlockingPhilosopher(Thread):
    def __init__(
        self, run_for: int, index: int, name: str, left: LockedFork, right: LockedFork
    ):
        super().__init__()
        self.run_for = run_for
        self.state = PhilosopherState.THINKING
        self.index = index
        self.name = name
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
            # This will eventually cause a deadlock as the left and right forks
            # can be picked up by different philosophers
            with self.left.semaphore, self.right.semaphore:
                self.state = PhilosopherState.EATING
                _logger.info(
                    f"{self.name} is eating with {self.left.name} and {self.right.name}"
                )
                time.sleep(STATE_TIME)
            time_now = datetime.now()


def start(run_for: int = None):
    forks = [
        LockedFork(i, f"Fork #{i + 1}", BoundedSemaphore()) for i in range(FORK_COUNT)
    ]
    philosophers = []
    for i in range(PHILOSOPHER_COUNT):
        philosophers.append(
            DeadlockingPhilosopher(
                run_for,
                i,
                f"Philosopher #{i + 1}",
                forks[i % FORK_COUNT],
                forks[(i + 1) % FORK_COUNT],
            )
        )

    for i in range(PHILOSOPHER_COUNT):
        philosophers[i].start()
