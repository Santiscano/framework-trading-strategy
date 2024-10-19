import MetaTrader5 as mt5

from utils.utils import Utils
from utils.colored_print import print_error
from data_provider.data_provider import DataProvider
from events.events import SignalEvent
from ..interfaces.position_sizer_interface import IPositionSizer

class MinSizePositionSizer(IPositionSizer):
    
    def size_signal(self, signal_event: SignalEvent, data_provider: DataProvider) -> float:
        volume = mt5.symbol_info(signal_event.symbol).volume_min
        
        if volume is not None:
            return volume
        else:
            print_error(F"{Utils.dateprint()} (MinSizePositionSizer): No se ha podido determinar el volumen mínimo para {signal_event.symbol}")
            return 0.0