import MetaTrader5 as mt5
from datetime import datetime
from zoneinfo import ZoneInfo

class Utils():
    
    def __init__(self):
        """
        Initializes the object.
        """
        pass
    
    @staticmethod
    def dateprint() -> str:
        """
        Returns the current date and time in the format "dd/mm/yyyy HH:MM:SS.sss".
        The timezone used is "Asia/Nicosia".
        """
        return datetime.now(ZoneInfo("Asia/Nicosia")).strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]