from .base import LogicModule


class ThermalLogicModule(LogicModule):
    """Class for rules considering temperature"""
    _initial_temperature = 21.0

    def __init__(self):
        super().__init__()
        self.current_value = self._initial_temperature  # temperature in Celsius
