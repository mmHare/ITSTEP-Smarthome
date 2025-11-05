from logic_module.logic.base import LogicModule


class ThermalLogicModule(LogicModule):
    """Class for rules considering temperature"""
    _initial_temperature = 21.0

    def __init__(self, controller):
        from logic_module.models import LogicController

        if not isinstance(controller, LogicController):
            raise TypeError("controller must be a LogicController instance")

        super().__init__(controller)

        self.high_limit = self.controller.time_max
        self.low_limit = self.controller.time_min
        self.current_value = self.controller.numeric_value

        if self.current_value == None:
            self.current_value = self._initial_temperature  # temperature in Celsius

    def update_current_value(self, current_temp: float):
        try:
            current_temp = float(current_temp)
            self.current_value = current_temp
        except ValueError:
            print('Wrong value. Temperature should be numeric.')
        except Exception as e:
            print(f'Error while setting temperature:', e)

        return self.current_value
