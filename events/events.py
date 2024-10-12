from enum import Enum
from pydantic import BaseModel
import pandas as pd

# *=========== Definimos los tipos de Enums que se utilizaran
class EventType(str, Enum):
    """
    Enumeration class representing different types of events.
    
    Attributes:
        DATA: Represents a data event.
        SIGNAL: Represents a signal event.
        SIZING: Represents a sizing event.
        ORDER: Represents an order event.
        EXECUTION: Represents an execution event.
        PENDING: Represents a pending event.
    """
    DATA = "DATA"
    SIGNAL = "SIGNAL"
    SIZING = "SIZING"
    ORDER = "ORDER"
    EXECUTION = "EXECUTION"
    PENDING = "PENDING"

class SignalType(str, Enum):
    """
    Represents the type of a trading signal.
    """
    BUY = "BUY"
    SELL = "SELL"

class OrderType(str, Enum):
    """
    Represents the type of an order.
    """
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"


# *=========== Clase principal padre de todos los eventos
class BaseEvent(BaseModel):
    """
    Base class for all events.
    """
    event_type: EventType
    class Config:
        arbitrary_types_allowed = True


# *=========== Definición de los distintos tipos de eventos
# Evento de obtención de datos
class DataEvent(BaseEvent):
    """
    Represents an event that contains data for a specific symbol.
    Attributes:
        event_type (EventType): The type of the event (always EventType.DATA).
        symbol (str): The symbol associated with the data.
        data (pd.Series): The data associated with the event.
    """
    event_type: EventType = EventType.DATA
    symbol: str
    data: pd.Series


# Evento de ...
class SignalEvent(BaseEvent):
    """
    Represents a signal event in the trading system.

    Attributes:
        event_type (EventType): The type of the event.
        symbol (str): The symbol associated with the signal.
        signal (SignalType): The type of signal.
        target_order (OrderType): The type of order to be placed.
        target_price (float): The target price for the order.
        magic_number (int): The magic number associated with the signal.
        sl (float): The stop loss level for the order.
        tp (float): The take profit level for the order.
    """
    pass


# Evento de ...
class SizingEvent(BaseEvent):
    """
    Represents a sizing event.

    Attributes:
        event_type (EventType): The type of the event.
        symbol (str): The symbol associated with the event.
        signal (SignalType): The signal type of the event.
        target_order (OrderType): The target order type of the event.
        target_price (float): The target price of the event.
        magic_number (int): The magic number associated with the event.
        sl (float): The stop loss value of the event.
        tp (float): The take profit value of the event.
        volume (float): The volume of the event.
    """
    pass


# Evento de ...
class OrderEvent(BaseEvent):
    """
    Represents an order event.

    Attributes:
        event_type (EventType): The type of the event.
        symbol (str): The symbol of the order.
        signal (SignalType): The signal type of the order.
        target_order (OrderType): The target order type.
        target_price (float): The target price of the order.
        magic_number (int): The magic number associated with the order.
        sl (float): The stop loss level of the order.
        tp (float): The take profit level of the order.
        volume (float): The volume of the order.
    """
    pass


# Evento de ...
class ExecutionEvent(BaseEvent):
    """
    Represents an execution event that occurs when a trade is executed.

    Attributes:
        event_type (EventType): The type of the event (EXECUTION).
        symbol (str): The symbol of the executed trade.
        signal (SignalType): The type of signal that triggered the execution.
        fill_price (float): The price at which the trade was executed.
        fill_time (datetime): The timestamp of the trade execution.
        volume (float): The volume of the executed trade.
    """
    pass


# Evento de ...
class PlacedPendingOrderEvent(BaseEvent):
    """
    Represents an event for a placed pending order.

    Attributes:
        event_type (EventType): The type of the event (EventType.PENDING).
        symbol (str): The symbol of the order.
        signal (SignalType): The type of signal for the order.
        target_order (OrderType): The type of order to be placed.
        target_price (float): The target price for the order.
        magic_number (int): The magic number associated with the order.
        sl (float): The stop loss level for the order.
        tp (float): The take profit level for the order.
        volume (float): The volume of the order.
    """
    pass

