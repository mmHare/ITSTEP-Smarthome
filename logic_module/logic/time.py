import time
from .base import LogicModule


class TimeLogicModule(LogicModule):
    """Class for rules considering time"""

    def __init__(self):
        super().__init__()
        self.current_value = time.time()  # starts with creation time
