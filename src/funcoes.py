
from controller.controller_atividades import AtividadesTurmas
from controller.controller_servidor import ServidorClienteController
import string
import random

def gerar_id_unico(tamanho = 12):
    caracteres = string.digits
    id_unico = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return id_unico

def cadastrar_nova_atividade(caminhodb, celular_aluno, id_robo):
    # funcao: 231733863532
    print("Começou funcao cadastro nova atividade")
    # variaveis para o cadastro de uma atividade:
    ra_aluno = ServidorClienteController.buscar_variavel_cadastrada_cliente(caminhodb, id_robo, celular_aluno, "ra_aluno_cadastro_atividade")
    semestre_atividade = ServidorClienteController.buscar_variavel_cadastrada_cliente(caminhodb, id_robo, celular_aluno, "semestre_cadastro_atividade")
    semestre_periodo = ServidorClienteController.buscar_variavel_cadastrada_cliente(caminhodb, id_robo, celular_aluno, "semestre_periodo_cadastro_atividade")
    materia_atividade = ServidorClienteController.buscar_variavel_cadastrada_cliente(caminhodb, id_robo, celular_aluno, "materia_cadastro_atividade")
    titulo_atividade = ServidorClienteController.buscar_variavel_cadastrada_cliente(caminhodb, id_robo, celular_aluno, "titulo_cadastro_atividade")
    descricao_atividade = ServidorClienteController.buscar_variavel_cadastrada_cliente(caminhodb, id_robo, celular_aluno, "descricao_cadastro_atividade")
    plataforma_entrega_atividade = ServidorClienteController.buscar_variavel_cadastrada_cliente(caminhodb, id_robo, celular_aluno, "plataforma_entrega_cadastro_atividade")
    data_entrega_atividade = ServidorClienteController.buscar_variavel_cadastrada_cliente(caminhodb, id_robo, celular_aluno, "data_entrega_cadastro_atividade")
    key_atividade = gerar_id_unico()
    id_atividade = AtividadesTurmas.adicionar_nova_atividade(caminhodb, id_robo, celular_aluno, ra_aluno, semestre_atividade, semestre_periodo, materia_atividade, titulo_atividade, descricao_atividade, plataforma_entrega_atividade, data_entrega_atividade, key_atividade)
    print("Atividade criada:")
    print(id_atividade)
    if(id_atividade == None):
        mensagem_atividade_criada = "Não foi possível registrar a atividade - "+titulo_atividade+". Por favor, tente preencher os dados novamente."
    else:
        mensagem_atividade_criada = "Atividade registrada com sucesso, aguarde até em que um moderador ou representante confirme a atividade. O identificador da atividade é: "+str(key_atividade)+"."
    mensagens_retorno = [mensagem_atividade_criada]
    objRetorno = {"mensagens": mensagens_retorno}
    return objRetorno