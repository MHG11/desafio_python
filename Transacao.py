from abc import ABC, abstractproperty, abstractclassmethod
from Conta import Conta
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass
    
    
    
    def registrar(self, conta):
        self.conta = []