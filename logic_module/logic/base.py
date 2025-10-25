from logic_module.models import LogicController


class LogicModule:
    """Base class for rule controls"""

    def __init__(self, controller: LogicController):
        self.controller = controller

        self.__active = True
        self.__current_value = None
        self.__high_limit = None
        self.__low_limit = None

    @property
    def active(self) -> bool:
        return self.__active

    @active.setter
    def active(self, value: bool):
        self.__active = value

    @property
    def current_value(self):
        return self.__current_value

    @current_value.setter
    def currente_value(self, value):
        self.__current_value = value

    @property
    def high_limit(self):
        return self.__high_limit

    @high_limit.setter
    def high_limit(self, value):
        self.__high_limit = value

    @property
    def low_limit(self):
        return self.__low_limit

    @low_limit.setter
    def low_limit(self, value):
        self.__low_limit = value

    def check(self) -> bool:
        try:
            self.get_current_value()
            result = self.check_condition()
        except Exception as e:
            print(f'Error during checking limits: {e}')
            result = False
        return result

    def get_current_value(self):
        self.__current_value = 0

    def check_condition(self) -> bool:
        result = self.low_limit < self.current_value < self.high_limit
