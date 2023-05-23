import logging
import random
import string
from datetime import datetime, timedelta
from threading import Thread
from time import sleep

from concurrent_django.models import Scroll


_logger = logging.getLogger(__name__)
PROBLEM_SIZE = 100


def _random_note() -> str:
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(32)
    )


class ScrollWriter(Thread):
    def __init__(self, run_for: int, target_scroll_id):
        super().__init__()
        self.target_scroll_id = target_scroll_id
        self.run_for = run_for

    def run(self):
        time_now = datetime.now()
        end_time = time_now + timedelta(seconds=self.run_for)
        while time_now < end_time:
            scroll = Scroll.objects.select_for_update().get(id=self.target_scroll_id)
            scroll.update_text = _random_note()
            sleep(random.uniform(0, 0.10))
            scroll.save()
            _logger.info("Saved the scroll")
            time_now = datetime.now()


def start(run_for: int = None):
    writers = []
    scroll, created = Scroll.objects.get_or_create(name="mass_write_scroll")
    for i in range(PROBLEM_SIZE):
        writers.append(ScrollWriter(run_for, scroll.id))
    for writer in writers:
        writer.start()
    for writer in writers:
        writer.join()
