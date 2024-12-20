from enum import Enum
from pydantic import BaseModel
from datetime import datetime

import pandas as pd

from interfaces import symbolsType

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
    symbol: symbolsType
    data: pd.Series


# Evento de obtencion de datos para validar una señal
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
    event_type: EventType = EventType.SIGNAL
    symbol: symbolsType
    signal: SignalType # BUY - SELL
    target_order: OrderType # MARKET - LIMIT - STOP
    target_price: float
    magic_number: int
    sl: float
    tp: float


# Evento de definicion de tamaño de la operacion
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
    event_type: EventType = EventType.SIZING
    symbol: symbolsType
    signal: SignalType
    target_order: OrderType
    target_price: float
    magic_number: int
    sl: float
    tp: float
    volume: float


# Evento de generacion de orden segun señal y riesgo definido a asumir
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
    event_type: EventType = EventType.ORDER
    symbol: symbolsType
    signal: SignalType
    target_order: OrderType
    target_price: float
    magic_number: int
    sl: float
    tp: float
    volume: float


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
    event_type: EventType = EventType.EXECUTION
    symbol: symbolsType
    signal: SignalType
    fill_price: float
    fill_time: datetime
    volume: float


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
    event_type: EventType = EventType.PENDING
    symbol: str
    signal: SignalType
    target_order: OrderType
    target_price: float
    magic_number: int
    sl: float
    tp: float
    volume: float

