from logic_module.logic.base import LogicModule


class ThermalLogicModule(LogicModule):
    """Class for rules considering temperature"""
    _initial_temperature = 21.0

    def __init__(self, controller):
        from logic_module.models import LogicController

        if not isinstance(controller, LogicController):
            raise TypeError("controller must be a LogicController instance")

        super().__init__(controller)

        self.high_limit = self.controller.numeric_max
        self.low_limit = self.controller.numeric_min
        self.current_value = self.controller.numeric_value

        if self.current_value == None:
            self.current_value = self._initial_temperature  # temperature in Celsius

    def update_current_value(self):
        try:
            self.current_value = float(self.current_value)
        except ValueError:
            print('Wrong value. Temperature should be numeric.')
        except Exception as e:
            print(f'Error while setting temperature:', e)

        return self.current_value

    def check_condition(self) -> bool:
        try:
            if (not self.low_limit) and (not self.high_limit):  # if both are 0 - always satisfied
                return True
            if not self.current_value:
                raise ValueError("No current value")
            return self.low_limit < self.current_value < self.high_limit
        except Exception as e:
            print("Error while checking condition:", e)
            return False
