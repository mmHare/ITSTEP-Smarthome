import time

from .base import LogicModule


class TimeLogicModule(LogicModule):
    """Class for rules considering time"""

    def __init__(self, controller):
        from logic_module.models import LogicController

        if not isinstance(controller, LogicController):
            raise TypeError("controller must be a LogicController instance")

        super().__init__(controller)

        self.high_limit = self.controller.time_max
        self.low_limit = self.controller.time_min

    def update_current_value(self):
        self.current_value = time.time()
        return self.current_value
