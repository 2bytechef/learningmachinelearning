import random
from apps.conversation_hosts.jobs import Action, Thought


class Timer:
    def __init__(self, duration: int, thought: Thought, name: str = None):
        if not name:
            name = f"{action.__class__.__name__} - {duration}s:{random.randint(10000, 99999)}"
        
        self.name = name
        self.duration = duration
        self.action = action
        # self._stop_event = threading.Event()
        # self._timer_thread = threading.Thread(target=self._start_timer)
        # self._timer_thread.start()
