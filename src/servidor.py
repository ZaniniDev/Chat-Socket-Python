
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import json
import traceback
from controller.controller_perguntas import PerguntasController
from controller.controller_respostas import RespostasController
from controller.controller_robo import RoboController
from controller.controller_servidor import ServidorClienteController
from controller.controller_funcoes import FuncoesController
from datetime import datetime, timedelta

from funcoes import cadastrar_nova_atividade

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
                if(responde_cliente == True):
                    celular_cliente = respostaTratamento["celular_destinatario"]
                    celular_robo = respostaTratamento["celular_remetente"]
                    mensagens = respostaTratamento["mensagens_resposta"]
                    id_robo = respostaTratamento["id_robo"]
                    tentativa_resposta = respostaTratamento["tentativa_resposta"]
                    envia_mensagem_cliente(chave_acesso_cliente, celular_cliente, celular_robo, id_robo, mensagens, tentativa_resposta=tentativa_resposta)

        if msg != bytes("{quit}", "utf8"):
            pass
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[nomeclient + keyclient]
            broadcast(bytes("%s saiu do chat" % nomeclient, "utf8"))
            break

def envia_mensagem_cliente(chave_acesso_cliente, celular_cliente, celular_robo, id_robo, mensagens, tentativa_resposta = 1):
    #procura o socket do cliente
    
    print("Enviar mensagens")    
    #envia mensagem para o socket apropriado do cliente
    
    if(clients[chave_acesso_cliente]):
        sock = clients[chave_acesso_cliente]
        objMensagem = {"remetente": celular_robo, "destinatario": celular_cliente, "mensagens": mensagens, "id_robo": id_robo, "tentativa_resposta": tentativa_resposta}        
        msgJson = json.dumps(objMensagem, ensure_ascii=False)        
        msgByte = bytes(msgJson, "utf8")
        sock.send(msgByte)        
        for mensagem in mensagens:
            msg = mensagem["mensagem"]
            id_pergunta = mensagem["id_pergunta"]
            id_msg_pergunta = mensagem["id_mensagem_pergunta"]
            horario_mensagem_string = mensagem["horariomensagem"]
            horario_mensagem = string_para_datetime_br(horario_mensagem_string)
            tentativa_resposta = mensagem["tentativa_resposta"]
            mensagem_encerramento = mensagem["mensagem_encerramento"]
            ServidorClienteController.adicionar_nova_mensagem_robo(CAMINHO_DATABASE, celular_cliente, celular_robo, msg, id_robo, id_pergunta, id_mensagem_pergunta=id_msg_pergunta,horariomensagem=horario_mensagem, tentativa_resposta=tentativa_resposta, mensagem_encerramento=mensagem_encerramento )
                        
def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

def tratamento_mensagem_usuario(mensagemJson):
    # recebe mensagem
    pergunta_controller = PerguntasController(CAMINHO_DATABASE)
    funcoes_controller = FuncoesController(CAMINHO_DATABASE)

    mensagemJson = json.loads(mensagemJson)
    celular_cliente = mensagemJson["remetente"]
    celular_robo = mensagemJson["destinatario"]
    horariomensagem_formatado = mensagemJson["horariomensagem"]
    destinatariogrupo = mensagemJson["destinatariogrupo"]
    id_robo = 1
    mensagem_recebida = mensagemJson["mensagem"]    
    resposta_tratamento = {"responde_cliente": False, "id_robo": id_robo,  "id_pergunta": None, "finalizar_atendimento": False, "mensagens_resposta": [], "celular_destinatario": celular_cliente, "celular_remetente": celular_robo, "tentativa_resposta": 1}
    try:
        horariomensagem = string_para_datetime_br(horariomensagem_formatado)
    except:
        print("Data do horario da mensagem não está no formato valido BR:\n"+str(horariomensagem_formatado))
        horariomensagem = None
    # Verifica se mensagem está no padrão ou contexto de alguma mensagem
    
    ultima_mensagem_robo = procura_ultima_mensagem_robo(celular_cliente, celular_robo)
    encontrou_ultima_mensagem = ultima_mensagem_robo["encontrou"]
    id_ultima_pergunta = ultima_mensagem_robo["id_pergunta"]
    tentativa_ultima_pergunta = ultima_mensagem_robo["tentativa_resposta"]
    id_proxima_pergunta = ""
    mensagens_resposta = []
    # Se não existir ultima mensagem do robo ou a ultima pergunta é despedida, então selecione e "Pergunta Menu"
    if(encontrou_ultima_mensagem == False):
        # Procura pergunta menu
        id_pergunta_menu = procura_pergunta_menu_robo(id_robo)
        id_proxima_pergunta = id_pergunta_menu    

    existe_resposta_ultima_pergunta = existe_respostas_pergunta(id_ultima_pergunta)
    tipo_resposta = "" 
    encontrou_resposta = False
    tentativa_resposta = 1
    ultima_sequencia = 0
    if(existe_resposta_ultima_pergunta == True):
        respostas_pergunta = procura_respostas_pergunta(id_ultima_pergunta)  
        for resposta in respostas_pergunta:
            tipo_resposta = resposta.tipo_resposta
            id_proxima_pergunta_resposta = resposta.id_proxima_pergunta
            if(tipo_resposta == "opcao"):
                opcao = str(resposta.opcao).strip()
                mensagem_recebida_sep = mensagem_recebida.split(" ")
                for mensagem in mensagem_recebida_sep:
                    if mensagem == opcao:
                        encontrou_resposta = True
                        break
                if(encontrou_resposta == True):
                    id_proxima_pergunta = id_proxima_pergunta_resposta
                    break 
            elif(tipo_resposta == "variavel"):
                nome_variavel = resposta.variavel
                tipo_variavel = resposta.tipo_variavel                
                valor_variavel = mensagem_recebida.strip()
                #verificação da variavel
                if(valor_variavel == ""):
                    encontrou_resposta = False
                else:
                    encontrou_resposta = True
                    ServidorClienteController.salvar_variavel_resposta_cliente(CAMINHO_DATABASE, id_robo=id_robo, celular_remetente=celular_cliente, nome_variavel=nome_variavel, valor=valor_variavel)
                    print("Salvou a variavel ("+celular_cliente+") - "+nome_variavel+": "+valor_variavel)
                    id_proxima_pergunta = id_proxima_pergunta_resposta
                    break 
        if(encontrou_resposta == False):
            tentativa_resposta = tentativa_ultima_pergunta + 1
            mensagem_padrao_tentativa_resposta = "Desculpa, parece que sua resposta não é válida. Podemos tentar novamente?"
            ultima_sequencia += 1
            objMensagem = {
                "id_pergunta": id_ultima_pergunta,  
                "id_mensagem_pergunta": 0,              
                "mensagem": mensagem_padrao_tentativa_resposta, 
                "sequencia_mensagem": ultima_sequencia,
                "id_funcao": "",
                "params_funcao": "",
                "mensagem_encerramento": 0,
                "tentativa_resposta": tentativa_resposta,
                "horariomensagem": string_data_atual_datetime_br()}
            mensagens_resposta.append(objMensagem)            
            id_proxima_pergunta = id_ultima_pergunta
        
    
    print("ID proxima pergunta - "+str(id_proxima_pergunta))
    if(id_proxima_pergunta != ""):        
        mensagens_pergunta = pergunta_controller.listar_mensagens_pergunta(id_proxima_pergunta) 
        # ajustar aqui para o cadastro de nova atividade
        # sempre quando houver função, deve ser feito aqui o processamento da função 
        
        for mensagem_pergunta in mensagens_pergunta:
            usar_mensagem_padrao = True 
            id_funcao =  mensagem_pergunta.id_funcao
            id_pergunta = mensagem_pergunta.id_pergunta
            id_mensagem_pergunta =  mensagem_pergunta.id       
            mensagem = mensagem_pergunta.mensagem
            
            params_funcao = mensagem_pergunta.params_funcao
            mensagem_encerramento = 0
            tentativa_resposta = tentativa_resposta
            horariomensagem = string_data_atual_datetime_br()
            if(id_funcao != "" and id_funcao != None):
                key_funcao_backend = funcoes_controller.obter_key_backend_via_id(id_funcao)
                retorno_mensagens_funcao = []
                if(key_funcao_backend == None):
                    # se a função do backend nao existir, então deve pular para proxima mensagem
                    continue

                #231733863532 - Cadastro de novas atividades
                if(key_funcao_backend == "231733863532"):
                    retorno_funcao = cadastrar_nova_atividade(CAMINHO_DATABASE, celular_cliente, id_robo)
                    retorno_mensagens_funcao = retorno_funcao["mensagens"]


                if(len(retorno_mensagens_funcao) > 0):
                    usar_mensagem_padrao = False
                    for mensagem_funcao in retorno_mensagens_funcao:
                        ultima_sequencia += 1
                        objMensagem = {
                            "id_pergunta": id_pergunta,  
                            "id_mensagem_pergunta": id_mensagem_pergunta,              
                            "mensagem": mensagem_funcao, 
                            "sequencia_mensagem": ultima_sequencia,
                            "id_funcao": id_funcao,
                            "params_funcao": params_funcao,
                            "mensagem_encerramento": 0,
                            "tentativa_resposta": tentativa_resposta,
                            "horariomensagem": string_data_atual_datetime_br()
                        }
                        mensagens_resposta.append(objMensagem)
                
            if (usar_mensagem_padrao == True):
                ultima_sequencia += 1
                objMensagem = {
                    "id_pergunta": mensagem_pergunta.id_pergunta,  
                    "id_mensagem_pergunta": mensagem_pergunta.id,              
                    "mensagem": mensagem_pergunta.mensagem, 
                    "sequencia_mensagem": ultima_sequencia,
                    "id_funcao": mensagem_pergunta.id_funcao,
                    "params_funcao": mensagem_pergunta.params_funcao,
                    "mensagem_encerramento": 0,
                    "tentativa_resposta": tentativa_resposta,
                    "horariomensagem": string_data_atual_datetime_br()}
                mensagens_resposta.append(objMensagem)
        existe_resposta_pergunta = existe_respostas_pergunta(id_proxima_pergunta)  
        if(existe_resposta_pergunta == False):
            # procura mensagem de finalização de atendimento
            id_pergunta_encerramento = procura_pergunta_encerramento_atendimento(id_robo)
            # adiciona as mensagens de finalização de atendimento
            mensagens_pergunta = pergunta_controller.listar_mensagens_pergunta(id_pergunta_encerramento)
            ultima_sequencia += 1
            for mensagem_pergunta in mensagens_pergunta:
                objMensagem = {
                    "id_pergunta": mensagem_pergunta.id_pergunta,  
                    "id_mensagem_pergunta": mensagem_pergunta.id,              
                    "mensagem": mensagem_pergunta.mensagem, 
                    "sequencia_mensagem": ultima_sequencia,
                    "id_funcao": mensagem_pergunta.id_funcao,
                    "params_funcao": mensagem_pergunta.params_funcao,
                    "mensagem_encerramento": 1,
                    "tentativa_resposta": tentativa_resposta,
                    "horariomensagem": string_data_atual_datetime_br()}
                mensagens_resposta.append(objMensagem)

        resposta_tratamento["id_pergunta"] = id_proxima_pergunta
        resposta_tratamento["responde_cliente"] = True
        resposta_tratamento["mensagens_resposta"] = mensagens_resposta
        resposta_tratamento["finalizar_atendimento"] = False if existe_resposta_pergunta else True

    resposta_tratamento["tentativa_resposta"] = tentativa_resposta

    # # Salva no histórico do robo a pergunta selecionada
    
    # # Envia para o cliente a proxima pergunta do robo
    # Adiciona mensagem do usuário no bd
    ServidorClienteController.adicionar_nova_mensagem_usuario(CAMINHO_DATABASE, celular_cliente, celular_robo, id_robo, mensagem_recebida, horariomensagem, destinatariogrupo)
        
    return resposta_tratamento
        
def procura_ultima_mensagem_robo(celular_cliente, celular_robo):   
    result_ultima_mensagem_robo = ServidorClienteController.procura_ultima_mensagem_robo(CAMINHO_DATABASE, celular_cliente, celular_robo)
    print("Ultima mensagem robo:")
    print(result_ultima_mensagem_robo)
    ultima_mensagem = {"encontrou": False, "id_ultima_mensagem": None, "id_pergunta": None, "horariomensagem": None, "mensagem_encerramento": 0, "tentativa_resposta": 0}
    if result_ultima_mensagem_robo:
        for row in result_ultima_mensagem_robo:
            #id, id_pergunta, horariomensagem, mensagem_encerramento, tentativa_resposta
            ultima_mensagem["encontrou"] = True
            ultima_mensagem["id_ultima_mensagem"] = row[0]
            ultima_mensagem["id_pergunta"] = row[1]
            ultima_mensagem["horariomensagem"] = row[2]
            ultima_mensagem["mensagem_encerramento"] = row[3]
            ultima_mensagem["tentativa_resposta"] = row[4]
    return ultima_mensagem

def procura_pergunta_menu_robo(id_robo):
    result_pergunta_menu = ServidorClienteController.procura_pergunta_menu_robo(CAMINHO_DATABASE, id_robo)
    id_pergunta_menu = None
    if result_pergunta_menu:
        for row in result_pergunta_menu:
            id_pergunta_menu = row[0]
    return id_pergunta_menu

def procura_respostas_pergunta(id_pergunta):
    respostaController = RespostasController(CAMINHO_DATABASE)
    result_respostas_pergunta = respostaController.listar_respostas_por_pergunta(id_pergunta)
    return result_respostas_pergunta

def existe_respostas_pergunta(id_pergunta):
    respostaController = RespostasController(CAMINHO_DATABASE)
    existe_resposta = respostaController.existe_resposta_pergunta(id_pergunta)
    return existe_resposta

def procura_pergunta_encerramento_atendimento(id_robo):
    result_pergunta_encerramento = ServidorClienteController.procura_pergunta_encerramento_robo(CAMINHO_DATABASE, id_robo)
    id_pergunta_encerramento = None
    if result_pergunta_encerramento:
        for row in result_pergunta_encerramento:
            id_pergunta_encerramento = row[0]
    return id_pergunta_encerramento



clients = {}
clients_usuario = {}
clients_robo = {}
addresses = {}
CAMINHO_DATABASE = "C:\\Users\\victt\\Desktop\\Marcus\\Projetos\\Chatbot\\chatbotui\\db\\repository\\chatbot.db"
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
