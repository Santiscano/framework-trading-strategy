import MetaTrader5 as mt5
from datetime import datetime
from zoneinfo import ZoneInfo
from colorama import Fore, Style

import MetaTrader5 as mt5

# from .colored_print import print_exception, print_error
from interfaces.symbolsType import SymbolsType

class Utils():
    
    def __init__(self):
        """
        Initializes the object.
        """
        pass


    # Creamos nuestro método estático con el decorador @staticmethod
    @staticmethod
    def convert_currency_amount_to_another_currency(amount: float, from_ccy: str, to_ccy: str) -> float:
        """
        Converts the given amount from one currency to another.
        Args:
            amount (float): The amount to be converted.
            from_ccy (str): The currency code of the source currency.
            to_ccy (str): The currency code of the target currency.
        Returns:
            float: The converted amount.
        Raises:
            Exception: If the symbol is not available in the MT5 platform.
        """
        # Comprobamos si ambas divisas para la conversión son las mismas
        if from_ccy == to_ccy:
            return amount
        
        all_fx_symbols: list[SymbolsType] = [symbol.value for symbol in SymbolsType]
        
        # Convertimos las divisas a mayúsculas
        from_ccy = from_ccy.upper()
        to_ccy = to_ccy.upper()
        
        # Buscamosel símbolo que relaciona nuestra divisa origen con nuestra divisa destino (list comprehension)
        fx_symbol = tuple([symbol for symbol in all_fx_symbols if from_ccy in symbol and to_ccy in symbol])[0]
        fx_symbol_base = fx_symbol[:3] # Divisa base sera siempre los primeros 3 caracteres del símbolo
        
        # Recuperamos los últimos datos disponibles del fx_symbol
        try:
            tick = mt5.symbol_info_tick(fx_symbol)
            if tick is None:
                print_exception(f"El símbolo {fx_symbol} no está disponible en la plataforma MT5. Por favor, revísa los símbolos disponibles de tu broker.")
        except Exception as e:
            print_error(f"ERROR: No se pudo recuperar el último tick del símbolo {fx_symbol}. MT5 error: {mt5.last_error()}, Exception: {e}")
            return 0.0
        else:
            # Recuperamos el último precio disponible del símbolo
            last_price  = tick.bid
            
            # Convertimos la cantidad de la divisa origen a la divisa destino
            converted_amount = amount / last_price if fx_symbol_base == to_ccy else amount * last_price # si la divisa base es la divisa destino, dividimos, si no, multiplicamos
            return converted_amount


    @staticmethod
    def dateprint() -> str:
        """
        Returns the current date and time in the format "dd/mm/yyyy HH:MM:SS.sss".
        The timezone used is "Asia/Nicosia".
        """
        return datetime.now(ZoneInfo("Asia/Nicosia")).strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]



def print_error(message):
    print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")

def print_warning(message):
    print(f"{Fore.YELLOW}[WARNING] {message}{Style.RESET_ALL}")

def print_success(message):
    print(f"{Fore.GREEN}[SUCCESS] {message}{Style.RESET_ALL}")

def print_info(message):
    print(f"{Fore.BLUE}[INFO] {message}{Style.RESET_ALL}")
    
def print_exception(message):
    mt5.shutdown()
    raise Exception(f"{Fore.RED}[Exception] {Utils.dateprint()} - {message}{Style.RESET_ALL}")