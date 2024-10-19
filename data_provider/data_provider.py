from typing import Dict
from datetime import datetime
from queue import Queue
import MetaTrader5 as mt5
import pandas as pd

from utils.utils import print_exception, print_error
from utils.utils import Utils
from events.events import DataEvent

from interfaces.timeframeType import TimeframeType
from interfaces.symbolsType import SymbolsType

class DataProvider():

    def __init__(self, events_queue: Queue, symbol_list: list[SymbolsType], timeframe:TimeframeType) -> None:
        """
        Initialize the DataProvider object.

        Args:
            events_queue (Queue): The queue to store the events.
            symbol_list (list): The list of symbols to fetch data for.
            timeframe (str): The timeframe for the data.

        Attributes:
            events_queue (Queue): The queue to store the events.
            symbols (list): The list of symbols to fetch data for.
            timeframe (str): The timeframe for the data.
            last_bar_datetime (Dict[str, datetime]): A dictionary to store the last seen datetime for each symbol.
        """
        self.events_queue = events_queue # esto es una cola de eventos
        self.symbols: list[SymbolsType] = symbol_list
        self.timeframe: TimeframeType = timeframe
        # Creamos un diccionario para guardar el datetime de la última vela que habíamos visto para cada símbolo
        self.last_bar_datetime: Dict[SymbolsType, datetime] = {symbol: datetime.min for symbol in self.symbols} # se veria asi: {'EURUSD': datetime.min, 'USDJPY': datetime.min, ...}



    def _map_timeframes(self, timeframe: TimeframeType) -> int:
        """
        Maps a string timeframe to its corresponding integer value.
        Args:
            timeframe (str): The string representation of the timeframe.
        Returns:
            int: The integer value of the mapped timeframe.
        Raises:
            None
        """
        timeframe_mapping = {
            'M1': mt5.TIMEFRAME_M1,
            'M2': mt5.TIMEFRAME_M2,                        
            'M3': mt5.TIMEFRAME_M3,                        
            'M4': mt5.TIMEFRAME_M4,                        
            'M5': mt5.TIMEFRAME_M5,                        
            'M6': mt5.TIMEFRAME_M6,                        
            'M10': mt5.TIMEFRAME_M10,                       
            'M12': mt5.TIMEFRAME_M12,
            'M15': mt5.TIMEFRAME_M15,
            'M20': mt5.TIMEFRAME_M20,                       
            'M30': mt5.TIMEFRAME_M30,                       
            'H1': mt5.TIMEFRAME_H1,                          
            'H2': mt5.TIMEFRAME_H2,                          
            'H3': mt5.TIMEFRAME_H3,                          
            'H4': mt5.TIMEFRAME_H4,                          
            'H6': mt5.TIMEFRAME_H6,                          
            'H8': mt5.TIMEFRAME_H8,                          
            'H12': mt5.TIMEFRAME_H12,
            'D1': mt5.TIMEFRAME_D1,                       
            'W1': mt5.TIMEFRAME_W1,                       
            'MN1': mt5.TIMEFRAME_MN1,                       
        }
        try:
            return timeframe_mapping[timeframe]
        except:
            print_exception("Timeframe {timeframe} no es válido.")



    def get_latest_closed_bar(self, symbol: SymbolsType, timeframe: TimeframeType) -> pd.Series:
        """
        Retrieves the latest closed bar for a given symbol and timeframe.

        Args:
            symbol (str): The symbol to retrieve the bar data for.
            timeframe (str): The timeframe of the bars.

        Returns:
            pd.Series: The latest closed bar data as a pandas Series object.
        """ 
        # Definir los parámetros adecuados
        tf = self._map_timeframes(timeframe)
        from_position = 1
        num_bars = 1
        try:
            bars_np_array = mt5.copy_rates_from_pos(symbol, tf, from_position, num_bars) # Recuperamos un array de numpy con los datos de la última vela
            if bars_np_array is None:
                print_error(f"{Utils.dateprint()} - El símbolo {symbol} no existe o no se han podido recuperar su datos")
                return pd.Series() # Vamos a devolver una Series empty para que no de error en el código que lo llame
            
            bars_pd = pd.DataFrame(bars_np_array) # Convertimos el array de numpy en un DataFrame de pandas
            
            # Convertimos la columna time a datetime y la hacemos el índice
            bars_pd['time'] = pd.to_datetime(bars_pd['time'], unit='s')
            bars_pd.set_index('time', inplace=True)
            
            # Cambiamos nombres de columnas y las reorganizamos
            bars_pd.rename(columns={'tick_volume': 'tickvol', 'real_volume': 'vol'}, inplace=True) # inplace=True es para que modifique el DataFrame original
            bars_pd = bars_pd[['open', 'high', 'low', 'close', 'tickvol', 'vol', 'spread']] # cambiamos el orden de las columnas

        except Exception as e:
            print_exception(f"No se han podido recuperar los datos de la última vela de {symbol} {timeframe} - MT5 Error: {mt5.last_error()}, exception: {e}")
        
        else:
            # Si el DF está vacío, devolvemos una serie vacía
            if bars_pd.empty:
                return pd.Series()
            else:
                return bars_pd.iloc[-1] # retornamos la última fila del DataFrame que es la última vela cerrada



    def get_latest_closed_bars(self, symbol: SymbolsType, timeframe: TimeframeType, num_bars: int = 1) -> pd.DataFrame:
        """
        Retrieves the latest closed bars for a given symbol and timeframe.

        Args:
            symbol (str): The symbol to retrieve bars for.
            timeframe (str): The timeframe of the bars (e.g., 'M1', 'H1', 'D1').
            num_bars (int, optional): The number of bars to retrieve. Defaults to 1.

        Returns:
            pd.DataFrame: A DataFrame containing the latest closed bars data.

        Raises:
            Exception: If the data retrieval fails.

        """

        # Definir los parámetros adecuados
        tf = self._map_timeframes(timeframe)
        from_position = 1
        bars_count = num_bars if num_bars > 0 else 1

        # Recuperamos los datos de la última vela
        try:
            bars_np_array = mt5.copy_rates_from_pos(symbol, tf, from_position, bars_count)
            if bars_np_array is None:
                print_error(f"{Utils.dateprint()} - El símbolo {symbol} no existe o no se han podido recuperar su datos")
                # Vamos a devolver un DataFrame empty
                return pd.DataFrame()

            bars = pd.DataFrame(bars_np_array)

            # Convertimos la columna time a datetime y la hacemos el índice
            bars['time'] = pd.to_datetime(bars['time'], unit='s')
            bars.set_index('time', inplace=True)

            # Cambiamos nombres de columnas y las reorganizamos
            bars.rename(columns={'tick_volume': 'tickvol', 'real_volume': 'vol'}, inplace=True)
            bars = bars[['open', 'high', 'low', 'close', 'tickvol', 'vol', 'spread']]
        
        except Exception as e:
            print_exception(f"No se han podido recuperar los datos de la última vela de {symbol} {timeframe} - MT5 Error: {mt5.last_error()}, exception: {e}")
        
        else:
            # Si todo OK, devolvemos el dataframe con las num_bars
            return bars



    def get_latest_tick(self, symbol: SymbolsType) -> dict:
        """
        Retrieves the latest tick for the given symbol.

        Parameters:
        symbol (str): The symbol for which to retrieve the latest tick.

        Returns:
        dict: A dictionary containing the latest tick information.
        """
        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                print_error(f"No se ha podido recuperar el último tick de {symbol} - MT5 error: {mt5.last_error()}")
                return {}
        
        except Exception as e:
            print_exception(f"Algo no ha ido bien a la hora de recuperar el último tick de {symbol}. MT5 error: {mt5.last_error()}, exception: {e}")
        
        else:
            return tick._asdict() # _asdict() es un metodo de mt5 para convertir el objeto en un diccionario de python



    def check_for_new_data(self) -> None:
        """
        Checks for new data for each symbol and adds it to the events queue if available.

        This method iterates over the symbols and checks if there is new data available for each symbol.
        If new data is found, it updates the last retrieved bar for the symbol and adds a DataEvent to the events queue.

        Returns:
            None
        """
        # 1- Comprobar si hay datos nuevos para cada símbolo
        for symbol in self.symbols:
            # Acceder a sus últimos datos disponibles, es una serie de pandas pero se puede acceder con el punto, sus valores para acceder serian open, high, low, close, tickvol, vol, spread
            latest_bar = self.get_latest_closed_bar(symbol, self.timeframe) 
            
            if latest_bar is None:
                continue
            
            # *si hay datos, se agrega un evento a la cola de eventos, esto para cada símbolo
            # latest_bar.name es el datetime - es decir si la nueva vela tiene una fecha mayor a la última vela que teníamos se ejecuta la condicion
            if not latest_bar.empty and latest_bar.name > self.last_bar_datetime[symbol]:
                self.last_bar_datetime[symbol] = latest_bar.name # Actualizar ultima vela recuperada
                data_event = DataEvent(symbol=symbol, data=latest_bar) # creamos DataEvent y lo añadimos a la cola de eventos
                self.events_queue.put(data_event)