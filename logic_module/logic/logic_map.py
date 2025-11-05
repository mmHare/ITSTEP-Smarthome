from .thermal import ThermalLogicModule
from .time import TimeLogicModule
from .base import LogicModule

LOGIC_MAP = {
    'none': LogicModule,
    'thermal': ThermalLogicModule,
    'time': TimeLogicModule,
}
