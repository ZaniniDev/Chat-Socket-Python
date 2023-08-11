
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import json
import traceback
from controller.controller_perguntas import PerguntasController
from controller.controller_robo import RoboController
from controller.controller_servidor import ServidorClienteController
from datetime import datetime, timedelta

def data_atual_datetime_br():
    # Obtém o datetime atual em UTC
    datetime_utc = datetime.utcnow()
    # Subtrai 3 horas do horario (HORARIO BRASILEIRO)
    datetime_brasil = datetime_utc - timedelta(hours=3)
    return datetime_brasil

def string_data_atual_datetime_br():
    # Obtém o datetime atual em UTC
    datetime_utc = datetime.utcnow()
    # Subtrai 3 horas do horario (HORARIO BRASILEIRO)
    datetime_brasil = datetime_utc - timedelta(hours=3)
    formato_brasil = "%d/%m/%Y %H:%M:%S"
    datetime_brasil_formatado = datetime_brasil.strftime(formato_brasil)
    return datetime_brasil_formatado

def string_para_datetime_br(string_horario_brasil):
    formato_brasil = "%d/%m/%Y %H:%M:%S"
    return datetime.strptime(string_horario_brasil, formato_brasil)

def receber_conexoes():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s está online." % client_address)
        addresses[client] = client_address
        Thread(target=receber_cliente, args=(client,)).start()


def receber_cliente(client):  # Takes client socket as argument.
    """Recebe o cliente."""

    boasvindas_client = client.recv(BUFSIZ).decode("utf8")
    print("Recebeu boas vindas cliente: "+str(boasvindas_client))
    print(boasvindas_client[0])
    respostaJson = {}
    try:
        respostaJson = json.loads(boasvindas_client)
    except:
        traceback.print_exc()
        print("Não foi possivel estabelecer conexão com o cliente -> "+str(client.getsockname))
        client.close()
        return
    print(respostaJson)
    nomeclient = respostaJson["client"]
    keyclient = respostaJson["keyclient"]
    tipoclient = respostaJson["tipoclient"]    
    client.send(bytes("Bem vindo "+nomeclient+"!", "utf8"))
    client.send(bytes("autorizado para enviar novas mensagens", "utf8"))
    # msg = "%s entrou no chat!" % name
    # broadcast(bytes(msg, "utf8"))
    if(tipoclient == "usuario"):
        clients_usuario[nomeclient + keyclient] = nomeclient
    elif(tipoclient == "robo"):
        clients_robo[nomeclient + keyclient] = nomeclient

    chave_acesso_cliente = nomeclient + "_" + keyclient
    clients[chave_acesso_cliente] = client
    
    id_robo = 1 #alterar para test

    while True:
        msg = client.recv(BUFSIZ)
        print("Recebeu nova mensage: "+str(msg))
        if(tipoclient == "usuario"):
            respostaTratamento = tratamento_mensagem_usuario(msg)
            if(respostaTratamento != None):
                responde_cliente = respostaTratamento["responde_cliente"]
                if(responde_cliente != True):
                    celular_cliente = respostaTratamento["celular_destinatario"]
                    celular_robo = respostaTratamento["celular_remetente"]
                    mensagens = respostaTratamento["mensagens_resposta"]
                    id_robo = respostaTratamento["id_robo"]
                    id_pergunta = respostaTratamento["id_pergunta"]
                    envia_mensagem_cliente(chave_acesso_cliente, celular_cliente, celular_robo, id_robo, mensagens, id_pergunta=id_pergunta)

        if msg != bytes("{quit}", "utf8"):
            pass
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[nomeclient + keyclient]
            broadcast(bytes("%s saiu do chat" % nomeclient, "utf8"))
            break

def envia_mensagem_cliente(chave_acesso_cliente, celular_cliente, celular_robo, id_robo, mensagens, id_pergunta = None, mensagem_encerramento = False):
    #procura o socket do cliente
    
    print("Enviar mensagens")    
    #envia mensagem para o socket apropriado do cliente
    
    if(clients[chave_acesso_cliente]):
        sock = clients[chave_acesso_cliente]
        print("Enviado mensagem - "+str(len(mensagens)))
        objMensagem = {"remetente": celular_robo, "destinatario": celular_cliente, "mensagens": mensagens, "id_robo": id_robo, "id_pergunta": id_pergunta}
        print(objMensagem)
        
        msgJson = json.dumps(objMensagem, ensure_ascii=False)        
        msgByte = bytes(msgJson, "utf8")
        sock.send(msgByte)
        
        for mensagem in mensagens:
            msg = mensagem["mensagem"]
            id_msg_pergunta = mensagem["id_mensagem_pergunta"]
            horario_mensagem_string = mensagem["horariomensagem"]
            horario_mensagem = string_para_datetime_br(horario_mensagem_string)
            ServidorClienteController.adicionar_nova_mensagem_robo(CAMINHO_DATABASE, celular_cliente, celular_robo, msg, id_robo, id_pergunta, id_mensagem_pergunta=id_msg_pergunta,horariomensagem=horario_mensagem, mensagem_encerramento=mensagem_encerramento)
            
            
def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

def tratamento_mensagem_usuario(mensagemJson):
    # recebe mensagem
    mensagemJson = json.loads(mensagemJson)
    celular_cliente = mensagemJson["remetente"]
    celular_robo = mensagemJson["destinatario"]
    horariomensagem_formatado = mensagemJson["horariomensagem"]
    destinatariogrupo = mensagemJson["destinatariogrupo"]
    id_robo = 1
    mensagem_recebida = mensagemJson["mensagem"]    
    resposta_tratamento = {"responde_cliente": False, "id_robo": id_robo,  "id_pergunta": None, "mensagens_resposta": [], "celular_destinatario": celular_cliente, "celular_remetente": celular_robo}
    try:
        horariomensagem = string_para_datetime_br(horariomensagem_formatado)
    except:
        print("Data do horario da mensagem não está no formato valido BR:\n"+str(horariomensagem_formatado))
        horariomensagem = None
    # Verifica se mensagem está no padrão ou contexto de alguma mensagem
    
    id_ultima_pergunta = procura_ultima_pergunta_robo(celular_cliente, celular_robo)
    
    # Se não existir ultima mensagem do robo ou a ultima pergunta é despedida, então selecione e "Pergunta Menu"
    if(id_ultima_pergunta == None):
        # Procura pergunta menu
        id_pergunta_menu = procura_pergunta_menu_robo(id_robo)
        pergunta_controller = PerguntasController(CAMINHO_DATABASE)
        mensagens_pergunta = pergunta_controller.listar_mensagens_pergunta(id_pergunta_menu)
        mensagens_texto = []
        for mensagem_pergunta in mensagens_pergunta:
            objMensagem = {
                "id_pergunta": mensagem_pergunta.id_pergunta,  
                "id_mensagem_pergunta": mensagem_pergunta.id,              
                "mensagem": mensagem_pergunta.mensagem, 
                "sequencia_mensagem": mensagem_pergunta.sequencia_mensagem,
                "id_funcao": mensagem_pergunta.sequencia_mensagem,
                "params_funcao": mensagem_pergunta.params_funcao,
                "horariomensagem": string_data_atual_datetime_br()}
            mensagens_texto.append(objMensagem)
        resposta_tratamento["id_pergunta"] = id_pergunta_menu
        resposta_tratamento["responde_cliente"] = True
        resposta_tratamento["mensagens_resposta"] = mensagens_texto
    
    # # Salva no histórico do robo a pergunta selecionada
    
    # # Envia para o cliente a proxima pergunta do robo
    # Adiciona mensagem do usuário no bd
    ServidorClienteController.adicionar_nova_mensagem_usuario(CAMINHO_DATABASE, celular_cliente, celular_robo, id_robo, mensagem_recebida, horariomensagem, destinatariogrupo)
        
    return resposta_tratamento
    
        
def procura_ultima_pergunta_robo(celular_cliente, celular_robo):
    result_ultima_mensagem_robo = ServidorClienteController.procura_ultima_mensagem_robo(CAMINHO_DATABASE, celular_cliente, celular_robo)
    print("Ultima pergunta robo:")
    print(result_ultima_mensagem_robo)
    id_ultima_mensagem = None
    if result_ultima_mensagem_robo:
        for row in result_ultima_mensagem_robo:
            id_ultima_mensagem = row[0]
            print(row[0])
            print("ID ultima mensagem robo - "+str(row[0]))   
    return id_ultima_mensagem

def procura_pergunta_menu_robo(id_robo):
    result_pergunta_menu = ServidorClienteController.procura_pergunta_menu_robo(CAMINHO_DATABASE, id_robo)
    id_pergunta_menu = None
    if result_pergunta_menu:
        for row in result_pergunta_menu:
            id_pergunta_menu = row[0]
            print(row[0])
            print("Pergunta Menu - "+str(row))
    return id_pergunta_menu



    

clients = {}
clients_usuario = {}
clients_robo = {}
addresses = {}
CAMINHO_DATABASE = "C:\\Users\\MarcusViniciusSoares\\OneDrive - GRANT THORNTON BRASIL\\Área de Trabalho\\Projetos\\ChatBotUniversal\\ChatBotUniversal\\chatbotui\\db\\repository\\chatbot.db"
HOST = "localhost"
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Esperando por conexões...")
    ACCEPT_THREAD = Thread(target=receber_conexoes)
    ACCEPT_THREAD.start()
    inputcontrole = input("Digite 1 para sair: ")
    if inputcontrole == "1":
        SERVER.close()
        exit(0)
    ACCEPT_THREAD.join()
    
SERVER.close()
