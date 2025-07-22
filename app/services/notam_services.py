class NotamContext:
    def __init__(self,strategy):
        self._strategy = strategy
    def get_Notam(self,retrieveLocId):
        return self._strategy.get_Notam(retrieveLocId)