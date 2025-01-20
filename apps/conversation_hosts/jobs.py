from typing import Any
from common.jobs import Action
from common.triggers import Trigger


class Speak(Action):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.super().__call__(*args, **kwds)
        
        print("Hello")

# class
