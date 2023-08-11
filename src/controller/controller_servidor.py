import json
import traceback
from socket import AF_INET, socket, SOCK_STREAM
from services.services_db import ServicoSQLite
from datetime import datetime, timedelta

class ServidorClienteController:
    def __init__(self):
        # caminhobd = "C:\\Users\\Victtoria\\OneDrive\\Desktop\\necessaryMarcus\\Projetos\\ChatBotUniversal\\database\\chatbot.db"
        # self.servicedb = ServicoSQLite(caminhobd)
        pass
    
    
    @classmethod
    def conectar_servidor_chatbot(self, host, port):
        try:
            ADDR = (host, port)
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect(ADDR)
            return client_socket
        except:
            traceback.print_exc()
            return None
        
    @classmethod 
    def enviar_mensagem_cliente_servidor_boasvindas(self, servidor, usuario, keyusuario):
        try:
            mensagemFinal = {
                "client": usuario,
                "keyclient": keyusuario,
                "tipoclient": "usuario"                               
            }
            
            msgJson = (json.dumps(mensagemFinal))
            msgByte = bytes(msgJson, "utf8")
            servidor.send(msgByte)
            return True
        except:
            traceback.print_exc()
            return False
    
    @classmethod
    def enviar_mensagem_cliente_servidor(self, servidor, remetente, destinatario, mensagem, horariomensagem, destinatariogrupo = ""):
        try:
            mensagemFinal = {
                "remetente": remetente,
                "destinatario": destinatario, 
                "mensagem": mensagem,                       
                "destinatariogrupo": destinatariogrupo,
                "horariomensagem": horariomensagem,
                "tiporemetente": "usuario" 
            }
            print(mensagemFinal)
            msgJson = json.dumps(mensagemFinal)
            msgByte = bytes(msgJson, "utf8")
            servidor.send(msgByte)
            return True
        except:
            traceback.print_exc()
            return False
    
    @classmethod
    def conectar_servidor(cls, host, port):
        try:
            ADDR = (host, port)
            server_socket = socket(AF_INET, SOCK_STREAM)
            server_socket.bind(ADDR)
            server_socket.listen(1)
            print("Aguardando conexão do cliente...")
            client_socket, client_address = server_socket.accept()
            print(f"Conexão estabelecida com {client_address}")
            return client_socket
        except:
            traceback.print_exc()
            return None
    
    @classmethod
    def receber_mensagem_cliente(cls, cliente):
        try:
            msg_byte = cliente.recv(4096)
            msg_json = msg_byte.decode("utf8")
            mensagem = json.loads(msg_json)
            return mensagem
        except:
            traceback.print_exc()
            return None
    
    @classmethod
    def enviar_mensagem_cliente(cls, cliente, mensagem):
        try:
            msg_json = json.dumps(mensagem)
            msg_byte = bytes(msg_json, "utf8")
            cliente.send(msg_byte)
            return True
        except:
            traceback.print_exc()
            return False

    @classmethod
    def criar_bd(self, caminhodb):
        servicedb = ServicoSQLite(caminhodb)
        servicedb.conectar()        
        # Query para criar a tabela
        queryTabelaMensagensUsuario = '''
            CREATE TABLE mensagens_usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                remetenteusuario TEXT,
                destinatariorobo TEXT,
                destinatariogrupo TEXT,
                horariomensagem DATETIME,
                dtCreate DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        '''
        queryTabelaMensagensRobos = '''
            CREATE TABLE mensagens_robos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                remetenterobo TEXT,
                destinatariousuario TEXT,
                destinatariogrupo TEXT,
                horariomensagem DATETIME,
                dtCreate DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        '''
        
        queryTabelaUsuarios = '''
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                apelido TEXT,
                celularprincipal TEXT,
                keyacesso TEXT,
                ativado INTEGER DEFAULT 1,
                dtCreate DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        '''
        
        queryTabelaRobos = '''
            CREATE TABLE robos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_criador INTEGER,
                nome TEXT,
                celular TEXT,
                ativado INTEGER DEFAULT 1,
                keyacesso TEXT DEFAULT NULL,
                dtCreate DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        '''
        
        queryTabelaPerguntasRobo = """
            CREATE TABLE perguntas_robos (
            id	INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo	TEXT,
            descricao TEXT,
            id_robo INTEGER,
            dtCreate DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        
        queryTabelaMensagensPerguntas = """
            CREATE TABLE mensagens_perguntas (
            id	INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pergunta INTEGER,
            mensagem TEXT,
            seq_mensagem INTEGER,
            id_funcao INTEGER,
            mensagem_despedida INTEGER DEFAULT 0,
            dtCreate DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        
        queryTabelaHistoricoPerguntas = """
            CREATE TABLE historico_perguntas (
            id	INTEGER PRIMARY KEY AUTOINCREMENT,
            id_rementeterobo INTEGER,
            id_destinatariousuario INTEGER,
            id_pergunta INTEGER,
            horariopergunta DATETIME,            
            dtCreate DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        
        queryTabelaRespostasRobos = """
            CREATE TABLE respostas_robos (
            id	INTEGER PRIMARY KEY AUTOINCREMENT,
            id_robo INTEGER,
            mensagem TEXT,
            tipo_resposta TEXT,          
            dtCreate DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        
        queryTabelaPerguntasRespostas = """
            CREATE TABLE perguntas_respostas (
            id	INTEGER PRIMARY KEY AUTOINCREMENT,
            id_robo INTEGER,
            id_pergunta INTEGER,
            id_resposta INTEGER,
            id_proximapergunta INTEGER,  
            dtCreate DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        
        queryTabelaPerguntaMenu = """
            CREATE TABLE pergunta_menu (
            id	INTEGER PRIMARY KEY AUTOINCREMENT,
            id_robo INTEGER,
            id_pergunta INTEGER, 
            dtCreate DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        # Executar a query
        # print(servicedb.executar_query(queryTabelaMensagensUsuario))
        # print(servicedb.executar_query(queryTabelaMensagensRobos))
        # print(servicedb.executar_query(queryTabelaUsuarios))
        # print(servicedb.executar_query(queryTabelaRobos))
        # print(servicedb.executar_query(queryTabelaPerguntasRobo))
        # print(servicedb.executar_query(queryTabelaMensagensPerguntas))
        # print(servicedb.executar_query(queryTabelaHistoricoPerguntas))
        # print(servicedb.executar_query(queryTabelaRespostasRobos))
        # print(servicedb.executar_query(queryTabelaPerguntasRespostas))
        # print(servicedb.executar_query(queryTabelaPerguntaMenu))
        servicedb.desconectar()
    
    @classmethod
    def adicionar_nova_mensagem_usuario(self, caminhodb, celular_usuario, celular_robo, id_robo, mensagem, horariomensagem = None, destinatariogrupo = None):
        servicedb = ServicoSQLite(caminhodb)
        servicedb.conectar()  
        remetente_robo = 0 #1 = verdadeiro 0 - falso
        if(horariomensagem == None or horariomensagem == ""):
            # Obtém o datetime atual em UTC
            datetime_utc = datetime.utcnow()
            # Subtrai 3 horas do horario (HORARIO BRASILEIRO)
            datetime_brasil = datetime_utc - timedelta(hours=3)
            horariomensagem = datetime_brasil
        colunasInsert = ["celular_remetente", "celular_destinatario", "mensagem", "horariomensagem", "remetente_robo", "id_robo"]
        valoresInsert = [celular_usuario, celular_robo, mensagem, horariomensagem, remetente_robo, id_robo]
        servicedb.executar_insert("historico_mensagens", colunasInsert, valoresInsert)
        servicedb.desconectar() 
        return True
    
    @classmethod
    def adicionar_nova_mensagem_robo(self, caminhodb, celular_usuario, celular_robo, mensagem, id_robo, id_pergunta, id_mensagem_pergunta, horariomensagem = None, mensagem_encerramento = False, destinatariogrupo = None):
        servicedb = ServicoSQLite(caminhodb)
        servicedb.conectar() 
        if(horariomensagem == None or horariomensagem == ""):
            # Obtém o datetime atual em UTC
            datetime_utc = datetime.utcnow()
            # Subtrai 3 horas do horario (HORARIO BRASILEIRO)
            datetime_brasil = datetime_utc - timedelta(hours=3)
            horariomensagem = datetime_brasil
        remetente_robo = 1
        colunasInsert = ["celular_remetente", "celular_destinatario", "mensagem", "horariomensagem", "remetente_robo", "id_robo", "id_pergunta", "id_mensagem_pergunta"]
        valoresInsert = [celular_robo, celular_usuario, mensagem, horariomensagem, remetente_robo, id_robo, id_pergunta, id_mensagem_pergunta]
        servicedb.executar_insert("historico_mensagens", colunasInsert, valoresInsert)
        servicedb.desconectar() 
        return True
    
    @classmethod
    def procura_ultima_mensagem_robo(self, caminhodb, celular_cliente, celular_robo):
        servicedb = ServicoSQLite(caminhodb)
        servicedb.conectar()  
        #procura o usuario pelo celular
        query_ultima_mensagem_usuario = """
            SELECT id, id_pergunta, horariomensagem, mensagem_encerramento
                FROM historico_mensagens
                WHERE celular_destinatario = ? and celular_remetente = ?
                ORDER BY horariomensagem DESC
                LIMIT 1;
        """
        ultima_mensagem = servicedb.executar_query(query_ultima_mensagem_usuario, [celular_cliente, celular_robo])      
        servicedb.desconectar() 
        return ultima_mensagem
    
    @classmethod
    def procura_pergunta_menu_robo(self, caminhodb, id_robo):
        servicedb = ServicoSQLite(caminhodb)
        servicedb.conectar()  
        #procura o usuario pelo celular
        query_pergunta_menu_robo = """
            SELECT id_pergunta
                FROM pergunta_menu
                WHERE id_robo = ?
                LIMIT 1;
        """
        id_pergunta = servicedb.executar_query(query_pergunta_menu_robo, [id_robo])       
        servicedb.desconectar() 
        return id_pergunta
    
    