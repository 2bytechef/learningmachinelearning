# from common.thread_cafe import ThreadCafe


from enum import Enum
from typing import Any


class Job:
    class Priority:
        INTERRUPT = 1
        RESPONSE = 2
        WAIT = 3
        
    class JobType(Enum):
        THOUGHT = 1
        ACTION = 2
        NOTIFICATION = 3

    priority: Priority = None
    is_synchronous: bool = False
    
    def __init__(self, priority: Priority, is_synchronous: bool = False):
        self.job_priority = priority
        self.is_synchronous = is_synchronous
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

class Thought(Job):
    type = Job.JobType.THOUGHT

class Action(Job):
    type = Job.JobType.ACTION

class Notification(Job):
    type = Job.JobType.NOTIFICATION
