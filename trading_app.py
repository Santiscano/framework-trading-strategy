from queue import Queue

from platform_connector.platform_connector import PlatformConnector
from data_provider.data_provider import DataProvider
from signal_generator.signal_generator import SignalGenerator
from signal_generator.properties.signal_generator_properties import MACrossoverProps, RSIProps
from position_sizer.position_sizer import PositionSizer
from position_sizer.properties.position_sizer_properties import MinSizingProps, FixedSizingProps, RiskPctSizingProps
from portfolio.portfolio import Portfolio

from trading_director.trading_director import TradingDirector

from interfaces.symbolsType import SymbolsType
from interfaces.timeframeType import TimeframeType

if __name__ == "__main__":
    
    # Definición de variables necesarias para la estrategia
    # symbols: list[SymbolsType] = ['EURUSD', 'USDJPY', 'GBPUSD', 'USDCAD']
    symbols: list[SymbolsType] = [SymbolsType.EURUSD, SymbolsType.USDJPY]
    timeframe: TimeframeType = 'M1'
    magic_number = 12345
    
    # Estrategia de cruce de medias móviles
    mac_props = MACrossoverProps(timeframe=timeframe,
                                fast_period=50,
                                slow_period=200)
    
    # Creación de la cola de eventos principales
    events_queue = Queue()
    
    # Creación de los modúlos principales del Framework
    CONNECT = PlatformConnector(symbols_list=symbols)
    DATA_PROVIDER = DataProvider(events_queue=events_queue,
                                symbol_list=symbols,
                                timeframe=timeframe)
    
    PORTFOLIO = Portfolio(magic_number=magic_number)
    # *Hasta aqui ya quedo funcional como el script final.
    
    SIGNAL_GENERATOR = SignalGenerator(events_queue=events_queue,
                                        data_provider=DATA_PROVIDER,
                                        portfolio=PORTFOLIO,
                                        # order_executor=ORDER_EXECUTOR,
                                        signal_properties=mac_props)
    
    POSITION_SIZER = PositionSizer(events_queue=events_queue,
                                    data_provider=DATA_PROVIDER,
                                    # sizing_properties=MinSizingProps())
                                    # sizing_properties=FixedSizingProps(volume=0.5))
                                    sizing_properties=RiskPctSizingProps(risk_pct=0.02)) # 2% del capital
    
    # Creación del director de trading y ejecución del bucle principal
    TRADING_DIRECTOR = TradingDirector(events_queue=events_queue,
                                        data_provider=DATA_PROVIDER,
                                        signal_generator=SIGNAL_GENERATOR,
                                        position_sizer=POSITION_SIZER)
    
    TRADING_DIRECTOR.execute()