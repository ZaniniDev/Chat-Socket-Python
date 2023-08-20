import json
import traceback
from services.services_db import ServicoSQLite
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

def string_para_datetime_br(horario_formatado_brasil):
    formato_brasil = "%d/%m/%Y %H:%M:%S"
    datetime_brasil_formatado = horario_formatado_brasil.strftime(formato_brasil)
    return datetime.strptime(datetime_brasil_formatado, formato_brasil)

def string_date_para_datetime_br(horario_formatado_brasil):
    try:
        # Define o formato da data brasileira
        formato_brasil = "%d/%m/%Y"
        
        # Converte a string da data para um objeto datetime
        datetime_brasil_formatado = datetime.strptime(horario_formatado_brasil, formato_brasil)
        
        return datetime_brasil_formatado
    except ValueError:
        print("Formato de data inválido. Certifique-se de usar o formato dd/mm/aaaa.")
        return None

class AtividadesTurmas:
    def __init__(self):
        # caminhobd = "C:\\Users\\Victtoria\\OneDrive\\Desktop\\necessaryMarcus\\Projetos\\ChatBotUniversal\\database\\chatbot.db"
        # self.servicedb = ServicoSQLite(caminhobd)
        pass
    
    @classmethod
    def adicionar_nova_atividade(self, caminhodb, id_robo, celular_aluno, ra_aluno, semestre_atividade, semestre_periodo, materia_atividade, titulo_atividade, descricao_atividade, plataforma_entrega_atividade, data_entrega_atividade, key_atividade):
        servicedb = ServicoSQLite(caminhodb)
        servicedb.conectar() 
        data_entrega_atividade_datetime = string_date_para_datetime_br(data_entrega_atividade)
        # Obtém o datetime atual em UTC
        datetime_utc = datetime.utcnow()
        # Subtrai 3 horas do horario (HORARIO BRASILEIRO)
        datetime_brasil = datetime_utc - timedelta(hours=3)
        colunasInsert = ["key_atividade", "id_robo", "celular_aluno", "ra_aluno", "semestre", "semestre_periodo", "materia", "titulo", "descricao", "plataforma_entrega", "data_entrega", "dt_create", "last_update"]
        valoresInsert = [key_atividade, id_robo, celular_aluno, ra_aluno, semestre_atividade, semestre_periodo, materia_atividade, titulo_atividade, descricao_atividade, plataforma_entrega_atividade, data_entrega_atividade_datetime, datetime_brasil, datetime_brasil]
        id_nova_atividade = servicedb.executar_insert("atividades_turmas", colunasInsert, valoresInsert)
        servicedb.desconectar() 
        return id_nova_atividade
    
    @classmethod
    def procura_pergunta_encerramento_robo(self, caminhodb, id_robo):
        servicedb = ServicoSQLite(caminhodb)
        servicedb.conectar()  
        #procura o usuario pelo celular
        query_pergunta_menu_robo = """
            SELECT id_pergunta_encerramento
                FROM robos
                WHERE id = ?
                LIMIT 1;
        """
        id_pergunta = servicedb.executar_query(query_pergunta_menu_robo, [id_robo])       
        servicedb.desconectar() 
        return id_pergunta
    
    @classmethod
    def buscar_variavel_cadastrada_cliente(self, caminhodb, id_robo, celular_remetente, nome_variavel):
        servicedb = ServicoSQLite(caminhodb)
        servicedb.conectar() 
        query_buscar_variavel = "SELECT valor FROM variaveis WHERE id_robo = ? and celular_remetente = ? and nome = ?"
        valores_query = [id_robo, celular_remetente, nome_variavel]
        valor_variavel = servicedb.executar_query(query_buscar_variavel, valores_query)     
        servicedb.desconectar() 
        return valor_variavel
    