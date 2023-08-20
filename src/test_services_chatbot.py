from unittest.mock import patch
import json
import os
import random
import string

from controller.controller_perguntas import PerguntasController
from controller.controller_respostas import RespostasController

def gerar_id_unico(tamanho = 12):
    caracteres = string.digits
    id_unico = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return id_unico

def input_resposta_variavel(id_pergunta, titulo_pergunta = ""):
    respostas_variaveis = []
    tipo_resposta = "variavel"
    opcao = 1
    nome_variavel = input("Digite o nome da variavel de resposta para a pergunta ("+str(id_pergunta)+") "+titulo_pergunta+":\n")
    nome_variavel = str(nome_variavel).lower().replace(" ","_").strip()
    desc_variavel = input("Explique o que é esta variável:\n")
    tipo_variavel = input("Digite se o valor da variavél deve ser: 1-Texto 2-Numero 3-Data 4-Hora 5-Data + Horario\n")
    if tipo_variavel == "1":
        tipo_variavel = "texto"
    elif tipo_variavel == "2":
        tipo_variavel = "numero"
    elif tipo_variavel == "3":
        tipo_variavel = "data"
    elif tipo_variavel == "4":
        tipo_variavel = "hora"
    elif tipo_variavel == "5":
        tipo_variavel = "datahora"
    else:
        tipo_variavel = "texto"
    id_proxima_pergunta_input = input("Digite o ID da proxima pergunta ou ENTER para não cadastrar proxima pergunta: \n")
    id_proxima_pergunta = None
    if(id_proxima_pergunta_input != None and id_proxima_pergunta_input != ""):
        try:
            id_proxima_pergunta = int(id_proxima_pergunta_input)
        except:
            print("O ID digitado não é valido! "+id_proxima_pergunta_input)
    respostas_variaveis.append({"id_pergunta": id_pergunta, "tipo_resposta": tipo_resposta, "variavel": nome_variavel, "tipo_variavel":tipo_variavel, "resposta": desc_variavel, "proxima_pergunta": id_proxima_pergunta})
    
    return respostas_variaveis

def input_resposta_opcoes(id_pergunta, titulo_pergunta = ""):
    #proxima pergunta = -2 -> Erro: a antiga pergunta foi removida
    #proxima pergunta = -1 -> Não foi configurada ainda
    #proxima pergunta = 0 -> Não existe proxima pergunta
    respostas_opcoes = []
    tipo_resposta = "opcao"
    opcao = 1
    opcaopergunta = "-1"
    while(opcaopergunta != "" and opcaopergunta != "0"):
        opcaopergunta = input("Digite a "+str(opcao)+"° opção da sua pergunta ("+str(id_pergunta)+") : "+titulo_pergunta+" ou pressione 0 para finalizar o cadastro de respostas:\n")        
        id_proxima_pergunta_input = input("Digite o ID da proxima pergunta ou ENTER para não cadastrar proxima pergunta: \n")
        id_proxima_pergunta = -1
        if(id_proxima_pergunta_input != "" and id_proxima_pergunta_input != "0"):
            try:
                id_proxima_pergunta = int(id_proxima_pergunta_input)
            except:
                print("O ID digitado não é valido! "+id_proxima_pergunta_input)
            id_proxima_pergunta = -1
        if(opcaopergunta != "" and opcaopergunta != "0"):
            respostas_opcoes.append({"id_pergunta": id_pergunta, "opcao": opcao, "tipo_resposta":tipo_resposta, "resposta": opcaopergunta, "proxima_pergunta": id_proxima_pergunta})
            opcao += 1
        else:
            break
    return respostas_opcoes

def ler_arquivojson(caminho):
    if os.path.exists(caminho) and os.path.getsize(caminho) > 0:
        # Se o arquivo existe e não está vazio, adicionamos uma vírgula e uma nova linha
        with open(caminho, 'r+', encoding="latin1") as json_file:
            conteudo = json_file.read()
            conteudo_separado = conteudo.split(";\n")
            print(len(conteudo_separado))

def escrever_arquivojson(caminho, objJson):
    if os.path.exists(caminho) and os.path.getsize(caminho) > 0:
        # Se o arquivo existe e não está vazio, adicionamos uma vírgula e uma nova linha
        with open(caminho, 'a+', encoding="latin1") as json_file:
            jsontxt = json.dumps(objJson)
            json_file.write(";\n")
            json_file.write(jsontxt)
            
    else:
        # Se o arquivo não existe ou está vazio, escrevemos o objeto JSON diretamente
        with open(caminho, 'w', encoding="latin1") as json_file:
            jsontxt = json.dumps(objJson)
            json_file.write(jsontxt)
            # json.dump([objJson], json_file, indent=4)

def cadastrar_novas_perguntas(caminhodbjson, caminhodbchatbot, id_robo):
    fluxo_perguntas_respostas = []
    
    fim_fluxo = False
    controllerPerguntas = PerguntasController(caminhodbchatbot)  
    respostas_controller = RespostasController(caminhodbchatbot)
  
    while(fim_fluxo == False):
        id_pergunta = gerar_id_unico()
        titulo_pergunta = ""    
        mensagens_pergunta = [] 
        respostas_pergunta = []   
        titulo_pergunta = input("Digite o titulo da pergunta:\n")
        descricao_pergunta = input("Digite a descrição para essa pergunta:\n")
        msg_pergunta = input("Digite a primeira mensagem da sua pergunta:\n")
        mensagens_pergunta.append(msg_pergunta)
        while msg_pergunta != "0":
            msg_pergunta = input("Digite a proxima mensagem da sua pergunta ou 0 para finalizar as mensagens:\n")
            if(msg_pergunta == "0" or msg_pergunta == ""):
                break
            mensagens_pergunta.append(msg_pergunta)
        confirmacao = input("Confirma a criação da pergunta: "+titulo_pergunta+"? Digite 1 para confirmar ou 0/ENTER para cancelar.")
        if(confirmacao == "1"):
            # Parte de cadastro das perguntas e respostas no banco de dados         

            # Cadastrando uma pergunta
            id_pergunta_cadastrada = controllerPerguntas.cadastrar_pergunta(id_robo=id_robo, titulo=titulo_pergunta, key_pergunta=id_pergunta, descricao=descricao_pergunta)
            print("Pergunta cadastrada: ", titulo_pergunta)
            print("ID da pergunta cadastrada:", id_pergunta_cadastrada)
            id_pergunta = id_pergunta_cadastrada
            
            # Cadastrando mensagens de uma pergunta
            for i in range(len(mensagens_pergunta)):
                mensagem = mensagens_pergunta[i]
                sequencia_mensagem = i + 1 
                cadastrou_mensagens = controllerPerguntas.adicionar_mensagem_pergunta(id_pergunta=id_pergunta_cadastrada, mensagem=mensagem, sequencia_mensagem=sequencia_mensagem)
                if(cadastrou_mensagens == False):
                    print("Não foi possivel cadastrar a mensagem da pergunta")
                    break
        else:
            print("Operação cancelada!")
            break
                
        perguntacomresposta = input("Digite 1 se essa pergunta tiver resposta ou 2 para finalizar esta pergunta:\n")
        if(perguntacomresposta == "2"):
            pass
        elif(perguntacomresposta == "1"):
            tipo_resposta = input("Digite o tipo de resposta. \n1 - Resposta com Opções. \n2 - Resposta para salvar variavel do cliente.\n")
            respostas = []
            #{"tipo_resposta":{"tipo":tipo_resposta, "opcao": opcao}, "mensagem": opcaopergunta, "proxima_pergunta": -1}
            if(tipo_resposta == "1"):            
                respostas = input_resposta_opcoes(id_pergunta, titulo_pergunta)
                confirmacao_respostas = input("Confirma a criação das respostas da pergunta: "+titulo_pergunta+"? Digite 1 para confirmar ou 0/ENTER para cancelar.")
                if(confirmacao_respostas == "1"):
                    # Parte de cadastro das perguntas e respostas no banco de dados 
                    for resposta in respostas:
                        tipo_resposta = resposta["tipo_resposta"]  # Tipo de resposta (por exemplo, "texto", "opção", "variável")
                        msg_resposta = resposta["resposta"]  # Conteúdo da resposta
                        opcao = str(resposta["opcao"])  # Se a resposta for do tipo "opção", aqui é informada a opção relacionada
                        id_resposta = respostas_controller.cadastrar_resposta(id_pergunta=id_pergunta, tipo_resposta=tipo_resposta, resposta=msg_resposta, opcao=opcao)
                else:
                    print("Operação cancelada!")
                    break
            elif(tipo_resposta == "2"):
                respostas = input_resposta_variavel(id_pergunta, titulo_pergunta)
                confirmacao_respostas = input("Confirma a criação das respostas da pergunta: "+titulo_pergunta+"? Digite 1 para confirmar ou 0/ENTER para cancelar.")
                if(confirmacao_respostas == "1"):
                    # Parte de cadastro das perguntas e respostas no banco de dados 
                    for resposta in respostas:
                        tipo_resposta = resposta["tipo_resposta"]  # Tipo de resposta (por exemplo, "texto", "opção", "variável")
                        descricao_variavel = resposta["resposta"]  # Conteúdo da resposta
                        nome_variavel = str(resposta["variavel"])  # Se a resposta for do tipo "opção", aqui é informada a opção relacionada
                        id_proxima_pergunta = resposta["proxima_pergunta"]
                        tipo_variavel = resposta["tipo_variavel"]
                        id_resposta = respostas_controller.cadastrar_resposta(id_pergunta=id_pergunta, tipo_resposta=tipo_resposta, resposta=descricao_variavel, variavel=nome_variavel, id_proxima_pergunta=id_proxima_pergunta, tipo_variavel=tipo_variavel)
                else:
                    print("Operação cancelada!")
                    break
                #fazer funcao para a resposta ser do para salvar uma variavel do cliente
                #vai salvar em uma tabela a parte chamada variaveis, com referencia ao cliente
                #campos: id_cliente, nomecliente, variavel, valor
                pass
            objPerguntaResposta = {
                "id_pergunta": id_pergunta,
                "titulo_pergunta": titulo_pergunta,
                "mensagens_pergunta": mensagens_pergunta,
                "respostas_pergunta": respostas,
                "id_proxima_pergunta": "-1"
            }            
            txtJson = {"id": id_pergunta, "perguntaresposta": objPerguntaResposta}
            print(txtJson)
            escrever_arquivojson(caminhodbjson, txtJson)            
            fluxo_perguntas_respostas.append(objPerguntaResposta)
            
        finalizarPeguntas = input("Deseja finalizar o cadastro? Digite uma das opções:\n1-Continuar cadastro\n0-Sair\n")
        if(finalizarPeguntas == "1"):
            id_pergunta = gerar_id_unico()
            continue
        else:
            break       
    pass

def listar_perguntas(caminhodbchatbot, id_robo):
    # Parte de cadastro das perguntas e respostas no banco de dados
    controller = PerguntasController(caminhodbchatbot)
    perguntas = controller.listar_perguntas_por_robo(id_robo)        
    return perguntas

def limpar_tabela(caminhodbchatbot):
    controller = PerguntasController(caminhodbchatbot)
    perguntas = controller.limpar_tabelas()       
    controllerRespostas = RespostasController(caminhodbchatbot)
    respostas = controllerRespostas.limpar_tabelas()
    return perguntas

def cadastrar_resposta(caminhodbchatbot, id_pergunta = ""):
    respostas_controller = RespostasController(caminhodbchatbot)
    perguntas_controller = PerguntasController(caminhodbchatbot)
    while True:
        if(id_pergunta == ""):
            id_pergunta = input("Digite o ID da pergunta que você quer cadastrar a resposta:\n")
        id_pergunta = int(id_pergunta)
        pergunta = perguntas_controller.obter_pergunta(id_pergunta)
        titulo_pergunta = pergunta.titulo
        perguntacomresposta = input("Digite 1 se essa pergunta tiver resposta ou 2 para finalizar esta pergunta:\n")
        if(perguntacomresposta == "2"):
            pass
        elif(perguntacomresposta == "1"):
            tipo_resposta = input("Digite o tipo de resposta. \n1 - Resposta com Opções. \n2 - Resposta para salvar variavel do cliente.\n")
            respostas = []
            #{"tipo_resposta":{"tipo":tipo_resposta, "opcao": opcao}, "mensagem": opcaopergunta, "proxima_pergunta": -1}
            if(tipo_resposta == "1"):            
                respostas = input_resposta_opcoes(id_pergunta, titulo_pergunta)
                confirmacao_respostas = input("Confirma a criação das respostas da pergunta: "+titulo_pergunta+"? Digite 1 para confirmar ou 0/ENTER para cancelar.")
                if(confirmacao_respostas == "1"):
                    # Parte de cadastro das perguntas e respostas no banco de dados 
                    for resposta in respostas:
                        tipo_resposta = resposta["tipo_resposta"]  # Tipo de resposta (por exemplo, "texto", "opção", "variável")
                        msg_resposta = resposta["resposta"]  # Conteúdo da resposta
                        opcao = str(resposta["opcao"])  # Se a resposta for do tipo "opção", aqui é informada a opção relacionada
                        id_proxima_pergunta = resposta["proxima_pergunta"]
                        id_resposta = respostas_controller.cadastrar_resposta(id_pergunta=id_pergunta, tipo_resposta=tipo_resposta, resposta=msg_resposta, opcao=opcao, id_proxima_pergunta=id_proxima_pergunta)
                else:
                    print("Operação cancelada!")
                    
                    return
            elif(tipo_resposta == "2"):
                respostas = input_resposta_variavel(id_pergunta, titulo_pergunta)
                confirmacao_respostas = input("Confirma a criação das respostas da pergunta: "+titulo_pergunta+"? Digite 1 para confirmar ou 0/ENTER para cancelar.")
                if(confirmacao_respostas == "1"):
                    # Parte de cadastro das perguntas e respostas no banco de dados 
                    print(respostas)
                    for resposta in respostas:
                        tipo_resposta = resposta["tipo_resposta"]  # Tipo de resposta (por exemplo, "texto", "opção", "variável")
                        descricao_variavel = resposta["resposta"]  # Conteúdo da resposta
                        nome_variavel = str(resposta["variavel"])  # Se a resposta for do tipo "opção", aqui é informada a opção relacionada
                        id_proxima_pergunta = resposta["proxima_pergunta"]
                        tipo_variavel = resposta["tipo_variavel"]
                        id_resposta = respostas_controller.cadastrar_resposta(id_pergunta=id_pergunta, tipo_resposta=tipo_resposta, resposta=descricao_variavel, variavel=nome_variavel, id_proxima_pergunta=id_proxima_pergunta, tipo_variavel=tipo_variavel)
                        print("Criou resposta - "+str(id_resposta))
                else:
                    print("Operação cancelada!")
                    break
                #fazer funcao para a resposta ser do para salvar uma variavel do cliente
                #vai salvar em uma tabela a parte chamada variaveis, com referencia ao cliente
                #campos: id_cliente, nomecliente, variavel, valor
                pass
            
        finalizarPeguntas = input("Deseja finalizar o cadastro? Digite uma das opções:\n1-Continuar cadastro\n0-Sair\n")
        if(finalizarPeguntas == "1"):
            id_pergunta = ""
            continue
        else:
            break

# Função para simular o input
def input_simulado(valores):
    return lambda _: valores.pop(0)

def test_cadastrar_novas_perguntas():
    caminhodbjson = "db\perguntas.txt"
    caminhodb_chatbot = "db\\repository\\chatbot.db"
    id_robo = 1
    # Executando a função cadastrar_novas_perguntas com entradas simuladas
    # Lista para armazenar os valores de entrada
    # valores_entrada_cadastro_perguntas_vagas = [
    #     "Menu de vagas",                                                # Título da primeira pergunta
    #     "Opções iniciais do meu menu",
    #     "Ola! Bem-vindo ao nosso sistema de busca de empregos",         # Primeira mensagem da pergunta 1
    #     "Digite uma das opcoes:",                                       # Segunda mensagem da pergunta 1
    #     "0",                                                            # Fim das mensagens da pergunta 1
    #     "1", #confirma criação das perguntas
    #     "1",                   # 1 - Pergunta com resposta 
        
    #     "1",                   # 1 - Tipo de resposta = Opcoes
    #     "Cadastrar vagas",     # Primeira opção da pergunta
    #     "Procurar vagas",      # Segunda opção da pergunta
    #     "0",                   # Finalizar opções
        
    #     "0"                    # Sair do cadastro
    # ]
    
    # with patch("builtins.input", input_simulado(valores_entrada_cadastro_perguntas_vagas)):
    #     cadastrar_novas_perguntas(caminhodbjson, caminhodb_chatbot, id_robo)
    
    valores_entrada_cadastro_perguntas_atletica = [
        "Menu auto atendimento atletica sistemas",                                                # Título da primeira pergunta
        "Perguntas iniciais de atendimento",
        "Bem vindo ao atendimento virtual da Atlética de Sistemas de informação e ADS da Unisanta.",         # Primeira mensagem da pergunta 1
        "Digite uma das opcoes para podermos te direcionar melhor:",                                       # Segunda mensagem da pergunta 1
        "1 - Informações sobre o Curso",
        "2 - Grupos da faculdade",
        "3 - Eventos e Atividades da Atlética",
        "4 - Horários de Aula",   
        "5 - Contatos Úteis",
        "0",                                                            # Fim das mensagens da pergunta 1
        "1", #confirma criação das perguntas
        
        "1",                   # 1 - Pergunta com resposta 
        
        "1",                   # 1 - Tipo de resposta = Opcoes
        "Informações sobre o Curso",
        "Grupos da faculdade",
        "Eventos e Atividades da Atlética",
        "Horários de Aula",   
        "Contatos Úteis",
        "0",                   # Finalizar opções
        "1", #confirma criação das respostas
        
        "0"                    # Sair do cadastro
    ]
    id_robo = 2
    with patch("builtins.input", input_simulado(valores_entrada_cadastro_perguntas_atletica)):
        cadastrar_novas_perguntas(caminhodbjson, caminhodb_chatbot, id_robo)

    ler_arquivojson(caminhodbjson)
    # # Executando a função cadastrar_novas_perguntas com entradas simuladas
    # with patch("builtins.input", input_simulado(valores_entrada)):
    #     cadastrar_novas_perguntas(caminhodbjson)

    # # Aqui você pode utilizar a lista valores_entrada com os inputs simulados como quiser
    # # Por exemplo, imprimir os valores simulados:
    # print("Valores simulados de entrada:", valores_entrada)

def test_listar_perguntas():
    caminhodbjson = "db\perguntas.txt"
    caminhodb_chatbot = "db\\repository\\chatbot.db"    
    id_robo = 1
    controller = PerguntasController(caminhodb_chatbot)
    
    perguntas = controller.listar_perguntas_por_robo(id_robo)  
    for pergunta in perguntas:            
        print(f"Robo ID: {pergunta.id_robo} Pergunta ID: {pergunta.id} Titulo: {pergunta.titulo}, Descricao: {pergunta.descricao} ")
    
    id_robo = 2
    perguntas = controller.listar_perguntas_por_robo(id_robo)
    for pergunta in perguntas:            
        print(f"Robo ID: {pergunta.id_robo} Pergunta ID: {pergunta.id} Titulo: {pergunta.titulo}, Descricao: {pergunta.descricao} ")
        mensagens = controller.listar_mensagens_pergunta(pergunta.id)
        for mensagem in mensagens:            
            print(f"Pergunta: {mensagem.id_pergunta} Mensagem ID: {mensagem.id}, Sequência: {mensagem.sequencia_mensagem}, Função: {mensagem.id_funcao}, Mensagem: {mensagem.mensagem}")
 
def test_limpar_tabela():
    limpar_tabela("db\\repository\\chatbot.db")
            

def input_cadastrar_novas_perguntas():
    caminhodbjson = "db\perguntas.txt"
    caminhodb_chatbot = "db\\repository\\chatbot.db"    
    id_robo = 1 #input("Digite o ID do robo")
    try:
        id_robo = int(id_robo)
    except:
        return
    cadastrar_novas_perguntas(caminhodbjson, caminhodb_chatbot, id_robo)

if __name__ == "__main__":
    # test_limpar_tabela()
    test_listar_perguntas()  
    caminhodb = "db\\repository\\chatbot.db"  
    servico_chatbot = input("Digite o serviço do chatbot para entrar: 1-Cadastrar novas perguntas, 2-Cadastrar novas respostas\n")
    if(servico_chatbot == "1"):
        input_cadastrar_novas_perguntas()
    elif(servico_chatbot == "2"):
        cadastrar_resposta(caminhodb)
    # test_cadastrar_novas_perguntas()