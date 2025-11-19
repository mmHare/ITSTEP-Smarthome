from datetime import datetime

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
        self.current_value = datetime.now().time()
        return self.current_value

    def time_in_range(self, start, end, current) -> bool:
        if start <= end:
            # Normal range (does not cross midnight)
            return start <= current <= end
        else:
            # Crosses midnight
            return current >= start or current <= end

    def check_condition(self) -> bool:
        try:
            if (not self.low_limit) or (not self.high_limit):
                raise ValueError("Limit is not set")
            elif (self.low_limit == self.high_limit):
                # limits have the same time -> check is off
                return True

            current_time = datetime.now().time()
            return self.time_in_range(self.low_limit, self.high_limit, current_time)
        except Exception as e:
            print("Error while checking condition:", e)
            return False
