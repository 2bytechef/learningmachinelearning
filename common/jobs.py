from enum import Enum
from typing import Any, Optional

from common.actors import Actor
from common.triggers import Trigger

# Jobs will need to be passed necessary context:
# - the actor that is thinking
# - the context of the conversation
# - the scene they will b e observing
# e
# other actors are not made aware of thoughts
# pass context object with actors and conversation history and scene
# return report =


class Job:
    class Priority:
        INTERRUPT = 1
        RESPONSE = 2
        WAIT = 3
        
    class JobType(Enum):
        OBSERVATION = 1
        THOUGHT = 2
        ACTION = 3
        NOTIFICATION = 4

    priority: Priority = None
    is_synchronous: bool = False
    
    def __init__(
        self,#, actor: Actor, priority: Priority, is_synchronous: bool = False
        # , trigger: Optional[Trigger] = None
        trigger: Job = None,
    ):
        # self.job_priority = priority
        # self.is_synchronous = is_synchronous
        # self.actor = actor
        self.trigger = trigger
        
    # we need to pass context and read result
    def __call__(self, check_stop_fn: function, *args: Any, **kwds: Any) -> Any:
        self.check_stop = check_stop_fn
        self.context = context
        
    def report(self):
        text = (
            f"Actor: {self.actor.name} performed the following action:\n"
            f"Job Type: {self.__class__.__name__}\nPriority: {self.priority}\nSynchronous: {self.is_synchronous}"
        )
    
    # def execute_fn(self) -> Any:
    #     pass

class Thought(Job):
    type = Job.JobType.THOUGHT

class Action(Job):
    type = Job.JobType.ACTION

class Notification(Job):
    type = Job.JobType.NOTIFICATION
