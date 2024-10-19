from enum import Enum

# Solo se permite usar divisas que esten en el broker
# !No usar comodities, indices, etc
class SymbolsType(str, Enum):
    """
    Enumeration class representing different types of symbols.
    """
    EURUSD = "EURUSD"
    GBPUSD = "GBPUSD"
    USDJPY = "USDJPY"
    USDCHF = "USDCHF"
    USDCAD = "USDCAD"
    AUDUSD = "AUDUSD"
    NZDUSD = "NZDUSD"
    EURJPY = "EURJPY"
    EURGBP = "EURGBP"
    EURCHF = "EURCHF"
    EURAUD = "EURAUD"
    EURCAD = "EURCAD"
    EURNZD = "EURNZD"
    XAUUSD = "XAUUSD"