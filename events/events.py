from enum import Enum
from pydantic import BaseModel
import pandas as pd

# Definición de los distintos tipos de eventos
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



class BaseEvent(BaseModel):
    """
    Base class for all events.
    """
    event_type: EventType

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