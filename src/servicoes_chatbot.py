

import json


def cadastrar_novas_perguntas(caminhodbjson):
    fluxo_conversa = {}
    #estrutura
    class PerguntaResposta:
        def __init__(self):
            self.fluxo_perguntasresposta = []
            self.id_pergunta = 1
            self.titulo_pergunta = ""
            self.mensagens_pergunta = []
            self.respostas_pergunta = []            
            pass
    fluxo_perguntas_respostas = []
    id_pergunta = 1
    titulo_pergunta = ""    
    mensagens_pergunta = [] 
    respostas_pergunta = []   
    fim_fluxo = False
    while(fim_fluxo == False):
        titulo_pergunta = input("Digite o titulo da pergunta:\n")
        msg_pergunta = input("Digite a primeira mensagem da sua pergunta:\n")
        mensagens_pergunta.append(msg_pergunta)
        while msg_pergunta != "0":
            msg_pergunta = input("Digite a proxima mensagem da sua pergunta ou 0 para finalizar as mensagens:\n")
            if(msg_pergunta == "0" or msg_pergunta == ""):
                break
            mensagens_pergunta.append(msg_pergunta)
        perguntacomresposta = input("Digite 1 se essa pergunta tiver resposta ou 2 para finalizar esta pergunta:\n")
        if(perguntacomresposta == "2"):
            objPerguntaResposta = {
                "id_pergunta": id_pergunta,
                "titulo_pergunta": titulo_pergunta,
                "mensagens_pergunta": mensagens_pergunta,
                "respostas_pergunta": [],
                "id_proxima_pergunta": "0"
            }
            id_pergunta += 1
            fluxo_perguntas_respostas.append(objPerguntaResposta)
        elif(perguntacomresposta == "1"):
            tipo_resposta = input("Digite o tipo de resposta. \n1 - Resposta com Opções. \n2 - Resposta para salvar variavel do cliente.\n")
            respostas = []
            #{"tipo_resposta":{"tipo":tipo_resposta, "opcao": opcao}, "mensagem": opcaopergunta, "proxima_pergunta": -1}
            if(tipo_resposta == "1"):            
                respostas = input_resposta_opcoes(id_pergunta, titulo_pergunta)
            elif(tipo_resposta == "2"):
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
            id_pergunta += 1
            txtJson = {"id": id_pergunta, "perguntaresposta": objPerguntaResposta}
            print(txtJson)
            with open(caminhodbjson, 'w') as json_file:
                json.dump(txtJson, json_file, indent=4)
            # fluxo_perguntas_respostas.append(objPerguntaResposta)
        print(fluxo_perguntas_respostas)        
    pass

def input_resposta_opcoes(id_pergunta, titulo_pergunta):
    #proxima pergunta = -2 -> Erro: a antiga pergunta foi removida
    #proxima pergunta = -1 -> Não foi configurada ainda
    #proxima pergunta = 0 -> Não existe proxima pergunta
    respostas_opcoes = []
    tipo_resposta = "opcao"
    opcao = 1
    opcaopergunta = input("Digite a "+str(opcao)+"° opção da sua pergunta '"+titulo_pergunta+"':\n")
    respostas_opcoes.append({"id_pergunta": id_pergunta, "tipo_resposta":tipo_resposta, "variaveis_resposta":{"opcao": opcao}, "mensagem": opcaopergunta, "proxima_pergunta": -1})
    opcao += 1
    while(opcaopergunta != "" and opcaopergunta != "0"):
        opcaopergunta = input("Digite a "+str(opcao)+"° opção da sua pergunta: "+titulo_pergunta+" ou pressione 0 para finalizar o cadastro de respostas:\n")        
        if(opcaopergunta != "" and opcaopergunta != "0"):
            respostas_opcoes.append({"tipo_resposta":{"tipo":tipo_resposta, "opcao": opcao}, "mensagem": opcaopergunta, "proxima_pergunta": -1})
            opcao += 1
        else:
            break
    return respostas_opcoes
    

CAMINHODBJSON = "C:\\Users\\MarcusViniciusSoares\\OneDrive - GRANT THORNTON BRASIL\\Área de Trabalho\\Projetos\\ChatBotUniversal\\ChatBotUniversal\\chatbotui\\db\\perguntas.json"
print("---------OPCOES----------")
print("1001 - Cadastrar nova pergunta")
print("1002 - Listar perguntas")
opcaoInput = input("Digite a opção:")

if(opcaoInput == "1001"):
    cadastrar_novas_perguntas(CAMINHODBJSON)

