import json
import traceback
from socket import AF_INET, socket, SOCK_STREAM
from services.services_db import ServicoSQLite


class ClientUsuarioController:
    def __init__(self):
        pass
        
    @classmethod
    def procuraUsuarioViaID(self, caminhobd, id):
        servicobd = ServicoSQLite(caminhobd)
        servicobd.conectar()
        queryProcuraUsuarioID = "Select * from usuarios where id = "+str(id)
        result = servicobd.executar_query(queryProcuraUsuarioID)
        servicobd.desconectar()
        return result
    
    
       
    