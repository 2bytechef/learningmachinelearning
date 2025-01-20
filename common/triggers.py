# class contains a list of classes
# the finishing job type which triggers it
# and the action that is triggered by this job type

from typing import List
from common.actors import Actor
from common.jobs import Job


class Trigger:
    def __init__(self, compatible_actors: List[Actor], trigger: Job, action: Job):
        self.compatible_actors = compatible_actors
        self.trigger = trigger
        self.action = action
