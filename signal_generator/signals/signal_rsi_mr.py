import pandas as pd
import numpy as np
import MetaTrader5 as mt5

from ..interfaces.signal_generator_interface import ISignalGenerator
from events.events import DataEvent
from data_provider.data_provider import DataProvider


class SignalRSI(ISignalGenerator):
    def __init__(self):
        super().__init__()
    
    def compute_rsi(self, prices: pd.Series) -> float:
        return 1
    
    def generate_signal(self, 
                        data_event: DataEvent, 
                        data_provider: DataProvider):
        pass