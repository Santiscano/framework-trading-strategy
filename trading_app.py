from queue import Queue

from platform_connector.platform_connector import PlatformConnector
from data_provider.data_provider import DataProvider
from trading_director.trading_director import TradingDirector

from interfaces.symbolsType import SymbolsType

if __name__ == "__main__":
    
    # Definición de variables necesarias para la estrategia
    symbols: list[SymbolsType] = ['EURUSD', 'USDJPY', 'GBPUSD', 'USDCAD']
    timeframe = '1min'
    
    
    # Creación de la cola de ventos principal
    events_queue = Queue()
    
    # Creación de los modúlos principales del Framework
    CONNECT = PlatformConnector(symbols_list=symbols)
    DATA_PROVIDER = DataProvider(events_queue=events_queue,
                                symbol_list=symbols,
                                timeframe=timeframe)
    
    # Creación del director de trading y ejecución del bucle principal
    TRADING_DIRECTOR = TradingDirector(events_queue=events_queue,
                                        data_provider=DATA_PROVIDER)
    
    TRADING_DIRECTOR.execute()