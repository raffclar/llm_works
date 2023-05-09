import logging

from concurrent_django.exercises.dining_philosophers.arbitration import start as start_arbitration_exercise
from concurrent_django.exercises.dining_philosophers.deadlock import start as start_deadlocking_exercise


_logger = logging.getLogger(__name__)


def main():
    _logger.info("Starting arbitration exercise")
    start_arbitration_exercise()
    _logger.info("Starting deadlocking exercise")
    start_deadlocking_exercise()


if __name__ == "__main__":
    logging.basicConfig()
    _logger.setLevel(logging.INFO)
    main()
