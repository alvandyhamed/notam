class NotamContext:
    def __init__(self,strategy):
        self._strategy = strategy
    def get_Notam(self,retrieveLocId,flight_number,user_id,date,rout):
        return self._strategy.get_Notam(retrieveLocId,flight_number,user_id,date,rout)