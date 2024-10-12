from typing import Dict, Callable
import queue
import time

from data_provider.data_provider import DataProvider

from events.events import DataEvent
from utils.colored_print import print_warning

class TradingDirector():
    
    def __init__(self, events_queue: queue.Queue, data_provider: DataProvider):
        """
        Initializes the TradingDirector object.

        Args:
            events_queue (queue.Queue): The queue to receive events.
            data_provider (DataProvider): The data provider object.
            signal_generator (ISignalGenerator): The signal generator object.
            position_sizer (PositionSizer): The position sizer object.
            risk_manager (RiskManager): The risk manager object.
            order_executor (OrderExecutor): The order executor object.
            notification_service (NotificationService): The notification service object.
        """
        self.events_queue = events_queue
        
        # Controlador de trading
        self.continue_trading: bool = True
        
        # Referencia a los distintos módulos
        self.DATA_PROVIDER = data_provider
        # ........
        
        # Creación del event handler
        self.event_handler: Dict[str, Callable] = {
            "DATA": self._handle_data_event,
            "SIGNAL": self._handle_signal_event,
            "SIZING": self._handle_sizing_event,
            "ORDER": self._handle_order_event,
            "EXECUTION": self._handle_execution_event,
            "PENDING": self._handle_pending_order_event,
        }
    
    def _handle_data_event(self, event: DataEvent):
        """
        Handle the data event.

        Args:
            event (DataEvent): The data event object.

        Returns:
            None
        """
        pass
    
    def _handle_signal_event(self, event):
        """
        Handle the signal event.

        Args:
            event (SignalEvent): The signal event object.

        Returns:
            None
        """
        pass
    
    def _handle_sizing_event(self, event):
        """
        Handle the sizing event.

        Args:
            event (SizingEvent): The sizing event object.

        Returns:
            None
        """
        pass

    def _handle_order_event(self, event):
        """
        Handle the order event.

        Args:
            event (OrderEvent): The order event object.

        Returns:
            None
        """
        pass
    
    def _handle_execution_event(self, event):
        """
        Handle the execution event.

        Args:
            event (ExecutionEvent): The execution event object.

        Returns:
            None
        """
        pass

    def _handle_pending_order_event(self, event):
        """
        Handle the pending order event.

        Args:
            event (PlacedPendingOrderEvent): The pending order event object.

        Returns:
            None
        """
        pass

    def _process_execution_or_pending_events(self, event):
        """
        Process the execution or pending events.

        Args:
            event (ExecutionEvent | PlacedPendingOrderEvent): The event to be processed.

        Returns:
            None
        """
        pass

    def _handle_none_event(self, event):
        """
        Handles the case when a None event is received.
        
        Prints an error message and sets `continue_trading` flag to False, terminating the execution of the Framework.
        
        Args:
            event: The None event received.
        """
        pass

    def _handle_unknown_event(self, event):
        """
        Handles the case when an Unknown event is received.
        
        Prints an error message and sets `continue_trading` flag to False, terminating the execution of the Framework.
        
        Args:
            event: The Unknown event received.
        """
        pass

    def execute(self) -> None:
        """
        Executes the main trading loop.

        This method continuously checks for events in the events queue and handles them accordingly.
        If no events are available, it checks for new data from the data provider.
        The loop continues until the `continue_trading` flag is set to False.

        Note:
        - The events are processed by the corresponding event handlers.
        - If an unknown event is encountered, it is handled by the `_handle_unknown_event` method.
        - If a None event is encountered, it is handled by the `_handle_none_event` method.

        Returns:
        None
        """
        # Definición del bucle principal
        while self.continue_trading:
            try:
                event = self.events_queue.get(block=False) # es una cola FIFO y block=False impide que se bloquee
            
            except queue.Empty:
                self.DATA_PROVIDER.check_for_new_data()
            
            else:
                if event is not None:
                    pass
                else:
                    pass
            
            time.sleep(0.01)
        
        print_warning("Trading Director stopped.")























