from datetime import datetime
import random

from apps.conversation_hosts.jobs import Action, Thought
from common.jobs import Job


class Timer:
    def __init__(self, duration: int, job: Job, name: str = None):
        if not name:
            name = f"{job.__class__.__name__} - {duration}s:{random.randint(10000, 99999)}"
        
        self.name = name
        self.duration = duration
        self.job = job
        
        self.last_start = datetime.now()
        # self._stop_event = threading.Event()
        # self._timer_thread = threading.Thread(target=self._start_timer)
        # self._timer_thread.start()
        
    def is_ready(self) -> bool:
        return (datetime.now() - self.last_start).seconds >= self.duration

    def reset(self):
        self.last_start = datetime.now()
        # self._stop_event.clear()
        # self._timer_thread = threading.Thread(target=self._start_timer)
        # self._timer_thread.start()