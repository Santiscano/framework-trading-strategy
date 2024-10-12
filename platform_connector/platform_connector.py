import os
from dotenv import load_dotenv, find_dotenv

import MetaTrader5 as mt5

from utils.utils import Utils
from utils.colored_print import print_error, print_info, print_success, print_warning, print_exception
from interfaces.symbolsType import SymbolsType

class PlatformConnector:
    def __init__(self, symbols_list: list[SymbolsType]) -> None:
        """
        Initializes the platform connector object.

        Args:
            symbol_list (list): List of symbols to be added to the MarketWatch.
        """
        load_dotenv(find_dotenv()) # Buscamos el archivo .env y cargamos sus valores
        self._initialize_platform() # Inicializamos la plataforma
        self._live_account_warning() # Mostramos una advertencia si la cuenta es real
        self._check_algo_trading_enabled() # Comprobamos si el trading algorítmico está activado
        self._add_symbols_to_marketwatch(symbols_list) # Añadimos los símbolos al MarketWatch
        self._print_account_info() # Mostramos la información de la cuenta



    def _initialize_platform(self) -> None:
        """"
        Initializes the MetaTrader5 platform with the environment variables
        
        Raises:
            Exception: If there is any error while initializing the platform

        Returns:
            None
        """
        try:
            if mt5.initialize(
                path=os.getenv("MT5_PATH"),
                login=int(os.getenv("MT5_LOGIN")),
                password=os.getenv("MT5_PASSWORD"),
                server=os.getenv("MT5_SERVER"),
                timeout=int(os.getenv("MT5_TIMEOUT")),
                portable=eval(os.getenv("MT5_PORTABLE"))
            ):
                print_success("Plataforma inicializada con éxito!")
            else:
                raise Exception(f"Error al inicializar la plataforma: {mt5.last_error()}")
        except Exception as e:
            print_exception(e)


    def _live_account_warning(self) -> None:
        """
        Displays a warning message if a real trading account is detected.
        Prompts the user to confirm if they want to continue.
        If the user chooses not to continue, the program is shut down.
        """
        try:
            trade_mode = mt5.account_info().trade_mode

            if trade_mode == mt5.ACCOUNT_TRADE_MODE_REAL:
                if not input("ALERTA: ESTA CUENTA ES REAL. ¿Deseas continuar? (y/n): ").lower() == "y":
                    mt5.shutdown()
                    raise Exception("Programa cerrado por el usuario.")
                else:
                    print_warning("Cuenta real detectada.")
            elif trade_mode == mt5.ACCOUNT_TRADE_MODE_DEMO:
                print_success("Cuenta demo detectada.")
            else:
                print_success("Cuenta tipo Concurso detectada.")
        except Exception as e:
            print_exception(e)



    def _check_algo_trading_enabled(self) -> None:
        """
        Checks if algorithmic trading is enabled.
        
        Raises:
            Exception: If algorithmic trading is disabled.
        """
        try:
            # vamos a comprobar que el trading algorítmico está activado
            if not mt5.terminal_info().trade_allowed:
                raise Exception("El trading algorítmico está desactivado. Por favor, actívalo MANUALMENTE desde la configuración del terminal MT5.")
        except Exception as e:
            print_exception(e)



    def _add_symbols_to_marketwatch(self, symbols: list[SymbolsType]) -> None:
        """
        Adds symbols to the MarketWatch if they are not already visible.

        Args:
            symbols (list): List of symbols to be added.

        Returns:
            None
        """
        for symbol in symbols:
            # 1) comprobamos si el simbolo existe
            if mt5.symbol_info(symbol) is None:
                print_error(f"{Utils.dateprint()} - No se ha podido añadir el símbolo {symbol} al MarketWatch: {mt5.last_error()}")
                continue
            
            # si el simbolo existe validamos si es visible
            if not mt5.symbol_info(symbol).visible:
                if not mt5.symbol_select(symbol, True):
                    print_error(f"{Utils.dateprint()} - No se ha podido añadir el símbolo {symbol} al MarketWatch: {mt5.last_error()}")
                else:
                    print_success(f"{Utils.dateprint()} - Símbolo {symbol} se ha añadido con éxito al MarketWatch!")
            else:
                print_success(f"{Utils.dateprint()} - El símbolo {symbol} ya estaba en el MarketWatch.")



    def _print_account_info(self) -> None:
        """
        Prints the account information including account ID, trader name, broker, server, leverage, currency, and balance.
        """
        # Recuperar un objeto de tipo AccountInfo
        account_info = mt5.account_info()._asdict()

        print_info(f"+------------ Información de la cuenta ------------")
        print_info(f"| - ID de cuenta: {account_info['login']}")
        print_info(f"| - Nombre trader: {account_info['name']}")
        print_info(f"| - Broker: {account_info['company']}")
        print_info(f"| - Servidor: {account_info['server']}")
        print_info(f"| - Apalancamiento: {account_info['leverage']}")
        print_info(f"| - Divisa de la cuenta: {account_info['currency']}")
        print_info(f"| - Balance de la cuenta: {account_info['balance']}")
        print_info(f"| - Agoritmo de trading: {account_info['trade_allowed']}")
        print_info(f"| - Experts advisors: {account_info['trade_expert']}")
        print_info(f"+--------------------------------------------------")
