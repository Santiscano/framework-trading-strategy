from typing import Dict, Callable
import queue
import time

from data_provider.data_provider import DataProvider
from position_sizer.position_sizer import PositionSizer
from signal_generator.interfaces.signal_generator_interface import ISignalGenerator

from events.events import DataEvent, SignalEvent
from utils.utils import print_warning, print_info, print_error
from utils.utils import Utils

class TradingDirector():
    
    def __init__(self, events_queue: queue.Queue, data_provider: DataProvider, signal_generator: ISignalGenerator,
                position_sizer: PositionSizer):
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
        self.SIGNAL_GENERATOR = signal_generator
        self.POSITION_SIZER = position_sizer
        # self.RISK_MANAGER
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
        # Aquí dentro gestionamos los eventos de tipo DataEvent
        print_info(f"{Utils.dateprint()} - Recibido DATA EVENT de {event.symbol} - Último precio de cierre: {event.data.close}")
        self.SIGNAL_GENERATOR.generate_signal(event)


    def _handle_signal_event(self, event: SignalEvent):
        """
        Handle the signal event.
        Args:
            event (SignalEvent): The signal event object.
        Returns:
            None
        """
        # Procesamos el signal event
        print_warning(f"{Utils.dateprint()} - Recibido SIGNAL EVENT de {event.symbol} - para la Señal: {event.signal}")
        self.POSITION_SIZER.size_signal(event)


    def _handle_sizing_event(self, event):
        """
        Handle the sizing event.
        Args:
            event (SizingEvent): The sizing event object.
        Returns:
            None
        """
        print_warning(f"{Utils.dateprint()} - Recibido SIZING EVENT con volumen {event.volume} para Señal: {event.signal} en {event.symbol}")
        # self.RISK_MANAGER

    def _handle_order_event(self, event):
        """
        Handle the order event.

        Args:
            event (OrderEvent): The order event object.

        Returns:
            None
        """
        print_warning(f"{Utils.dateprint()} - ")
    
    def _handle_execution_event(self, event):
        """
        Handle the execution event.

        Args:
            event (ExecutionEvent): The execution event object.

        Returns:
            None
        """
        print_warning(f"{Utils.dateprint()} - ")

    def _handle_pending_order_event(self, event):
        """
        Handle the pending order event.

        Args:
            event (PlacedPendingOrderEvent): The pending order event object.

        Returns:
            None
        """
        print_warning(f"{Utils.dateprint()} - ")

    def _process_execution_or_pending_events(self, event):
        """
        Process the execution or pending events.

        Args:
            event (ExecutionEvent | PlacedPendingOrderEvent): The event to be processed.

        Returns:
            None
        """
        print_warning(f"{Utils.dateprint()} - ")

    def _handle_none_event(self, event):
        """
        Handles the case when a None event is received.
        
        Prints an error message and sets `continue_trading` flag to False, terminating the execution of the Framework.
        
        Args:
            event: The None event received.
        """
        print_error(f"{Utils.dateprint()} - ERROR: Recibido evento nulo. Terminando ejecución del Framework")
        self.continue_trading = False

    def _handle_unknown_event(self, event):
        """
        Handles the case when an Unknown event is received.
        
        Prints an error message and sets `continue_trading` flag to False, terminating the execution of the Framework.
        
        Args:
            event: The Unknown event received.
        """
        print_error(f"{Utils.dateprint()} - ERROR: Recibido evento desconocido. Terminando ejecución del Framework. Evento: {event}")
        self.continue_trading = False

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
                # Extraemos un evento de la cola de eventos
                event = self.events_queue.get(block=False) # es una cola FIFO y block=False impide que se bloquee
            
            except queue.Empty:
                # Si no hay un evento en cola, caemos en el except y comprobamos si hay nuevos datos
                print(f"{Utils.dateprint()} - No hay eventos en cola. Comprobando nuevos datos...")
                self.DATA_PROVIDER.check_for_new_data()
            
            else:
                # si hay un evento en cola, lo procesamos
                if event is not None:
                    # extraemos el evento que tenga por clave el diccionario en event.event_type - "esto seria como hacer event_handler[event.event_type]"
                    handler = self.event_handler.get(event.event_type, self._handle_unknown_event) # event_handler es un diccionario, con el metodo get traemos el metodo, el primer parametro es la clave y el segundo es el valor por defecto si no encuentra la clave
                    handler(event) # ejecutamos el metodo handler que hizo match con el evento como parametro
                else:
                    self._handle_none_event(event) # se detendria el programa si se recibe un evento nulo
            
            # time.sleep(0.1)
            time.sleep(1) # !cambiar a 0.01 en producción
        
        print_warning("Trading Director stopped.")























