from queue import Queue

from platform_connector.platform_connector import PlatformConnector
from data_provider.data_provider import DataProvider
from trading_director.trading_director import TradingDirector
from signal_generator.signal_generator import SignalGenerator
from signal_generator.properties.signal_generator_properties import MACrossoverProps, RSIProps

from interfaces.symbolsType import SymbolsType
from interfaces.timeframeType import TimeframeType

if __name__ == "__main__":
    
    # Definición de variables necesarias para la estrategia
    # symbols: list[SymbolsType] = ['EURUSD', 'USDJPY', 'GBPUSD', 'USDCAD']
    symbols: list[SymbolsType] = [SymbolsType.EURUSD, SymbolsType.USDJPY]
    timeframe: TimeframeType = 'M1'
    
    # Estrategia de cruce de medias móviles
    mac_props = MACrossoverProps(timeframe=timeframe,
                                fast_period=50,
                                slow_period=200)
    
    # Creación de la cola de ventos principal
    events_queue = Queue()
    
    # Creación de los modúlos principales del Framework
    CONNECT = PlatformConnector(symbols_list=symbols)
    DATA_PROVIDER = DataProvider(events_queue=events_queue,
                                symbol_list=symbols,
                                timeframe=timeframe)
    
    SIGNAL_GENERATOR = SignalGenerator(events_queue=events_queue,
                                        data_provider=DATA_PROVIDER,
                                        signal_properties=mac_props)
    
    # Creación del director de trading y ejecución del bucle principal
    TRADING_DIRECTOR = TradingDirector(events_queue=events_queue,
                                        data_provider=DATA_PROVIDER,
                                        signal_generator=SIGNAL_GENERATOR)
    
    TRADING_DIRECTOR.execute()