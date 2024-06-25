from dataclasses import dataclass
import datetime
from Transacao import Transacao

@dataclass
class Historico:
    
    def __init__(self):
        self._transacoes = []
        
    @property
    def tansacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self):
       self._transacoes.append(
           {
               "Tipo": Transacao.__class__.__name__,
               "Valor": Transacao.valor,
               "Data": datetime.now().srtftime("%d-%m-%Y"),
           }
       ) 