from events.events import DataEvent, SignalEvent, SignalType
from data_provider.data_provider import DataProvider
from ..interfaces.signal_generator_interface import ISignalGenerator
from ..properties.signal_generator_properties import MACrossoverProps

from utils.utils import print_exception
from interfaces.symbolsType import SymbolsType

import pandas as pd
from queue import Queue

class SignalMACrossover(ISignalGenerator):
    def __init__(self, events_queue: Queue, data_provider: DataProvider, properties: MACrossoverProps):
        """
        Initializes the MACrossover object.

        Args:
            properties (MACrossoverProps): The properties object containing the parameters for the moving average crossover.

        Raises:
            Exception: If the fast period is greater than or equal to the slow period.

        """
        self.events_queue = events_queue
        self.DATA_PROVIDER = data_provider
        
        self.timeframe = properties.timeframe
        self.fast_period = properties.fast_period if properties.fast_period > 1 else 2
        self.slow_period = properties.slow_period if properties.slow_period >2 else 3 # slow period trae la cantidad de velas que se van a usar para calcular la media móvil
        
        if self.fast_period >= self.slow_period:
            print_exception("ERROR: el perdiodo rápido ({self.fast_period}) es mayor o igual al periodo lento ({self.slow_period}) para el cálculo de las medias móviles.")
    
    
    def _create_and_put_signal_event(self, symbol: SymbolsType, signal:SignalType, target_order:str, target_price:float, magic_number:int, sl:float, tp:float):
        # creamos un signal event
        signal_event = SignalEvent(symbol=symbol, 
                                signal=signal, 
                                target_order=target_order, 
                                target_price=target_price, 
                                magic_number=magic_number, 
                                sl=sl, 
                                tp=tp)
        # Ponemos el signal event en la cola de eventos
        self.events_queue.put(signal_event)
    
    
    def generate_signal(self, data_event: DataEvent, data_provider: DataProvider) -> SignalEvent:
        """
        Generates a signal based on the moving average crossover strategy.

        Args:
            data_event (DataEvent): The data event that triggered the signal generation.
            data_provider (DataProvider): The data provider used to retrieve the necessary data.
            portfolio (Portfolio): The portfolio containing the open positions.
            order_executor (OrderExecutor): The order executor used to execute the orders.

        Returns:
            SignalEvent: The generated signal event.
        """
        # Cogemos el símbolo del evento
        symbol = data_event.symbol

        # Recuperamos los datos necesarios para calcular las medias móviles
        bars = data_provider.get_latest_closed_bars(symbol, self.timeframe, self.slow_period)
        
        # Recuperamos las posiciones abiertas por esta estrategia en el símbolo donde hemos tenido el Data Event
        
        # Calculamos el valor de los indicadores
        fast_ma = bars['close'][-self.fast_period:].mean()
        slow_ma = bars['close'].mean()
        
        # Detectar una señal de compra
        if fast_ma > slow_ma:
            signal = "BUY"
        
        # Detectar una señal de venta
        elif slow_ma > fast_ma:
            signal = "SELL"
        
        else:
            signal = ""


        # Si tenemos señal, generamos SignalEvent y lo colocamos en la cola de Eventos
        if signal != "":
            signal_event = self._create_and_put_signal_event(symbol=symbol,
                                                            signal=signal,
                                                            target_order="MARKET",
                                                            target_price=0.0,
                                                            magic_number=1234,
                                                            sl=0.0,
                                                            tp=0.0)