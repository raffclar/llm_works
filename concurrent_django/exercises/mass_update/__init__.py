import logging
import random
import string
from threading import Thread
from time import sleep

from concurrent_django.models import Scroll


_logger = logging.getLogger(__name__)
PROBLEM_SIZE = 100


def _random_note() -> str:
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))


class ModelWriter(Thread):
    def __init__(self, target_scroll_id):
        super().__init__()
        self.target_scroll_id = target_scroll_id

    def run(self):
        while True:
            scroll = Scroll.objects.select_for_update().get(id=self.target_scroll_id)
            scroll.update_text = _random_note()
            sleep(random.uniform(0, 0.10))
            scroll.save()
            _logger.info("Saved")


def start(run_for: int = None):
    writers = []
    scroll, created = Scroll.objects.get_or_create(name="mega_write_scroll")
    for i in range(PROBLEM_SIZE):
        writers.append(ModelWriter(scroll.id))

    for writer in writers:
        writer.start()
