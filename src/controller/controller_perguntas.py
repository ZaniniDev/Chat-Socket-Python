import json
import traceback
from services.services_db import ServicoSQLite

from sqlalchemy import create_engine, Column, Integer, String, MetaData, DateTime, desc, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta

Base = declarative_base()

class Pergunta(Base):
    __tablename__ = 'perguntas_robos'
    # Obtém o datetime atual em UTC
    datetime_utc = datetime.utcnow()
    # Subtrai 3 horas do horario (HORARIO BRASILEIRO)
    datetime_brasil = datetime_utc - timedelta(hours=3)
    
    id = Column(Integer, primary_key=True)
    id_robo = Column(Integer)
    titulo = Column(String)
    descricao = Column(String)
    key_pergunta = Column(String)
    dt_create = Column(DateTime, default=datetime_brasil)
    last_update = Column(DateTime, default=datetime_brasil, onupdate=datetime_brasil)
    mensagens = relationship("MensagemPergunta", back_populates="pergunta")
    

class MensagemPergunta(Base):
    __tablename__ = 'mensagens_perguntas'
    id = Column(Integer, primary_key=True)
    id_pergunta = Column(Integer, ForeignKey('perguntas_robos.id'))
    mensagem = Column(String)
    sequencia_mensagem = Column(Integer, default=None)
    id_funcao = Column(Integer, default=None)
    params_funcao = Column(String, default=None)
    dt_create = Column(DateTime, default=datetime.utcnow)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    pergunta = relationship("Pergunta", back_populates="mensagens")

class PerguntasController:
    def __init__(self, caminhobd):
        self.caminhobd = caminhobd
        # Conecta ao banco de dados SQLite
        self.engine = create_engine(f'sqlite:///{caminhobd}')
        # Cria as tabelas no banco de dados (caso ainda não existam)
        Base.metadata.create_all(self.engine)
        # Cria uma fábrica de sessão para interagir com o banco de dados
        self.Session = sessionmaker(bind=self.engine)

    def cadastrar_pergunta(self, titulo, id_robo, key_pergunta, descricao=""):
        """Cadastra uma nova pergunta no banco de dados."""
        new_pergunta = Pergunta(id_robo=id_robo, titulo=titulo, descricao=descricao, key_pergunta=key_pergunta)
        session = self.Session()
        session.add(new_pergunta)
        session.commit()
        id_pergunta = new_pergunta.id
        session.close()
        return id_pergunta

    def excluir_pergunta(self, id_pergunta):
        """Exclui uma pergunta do banco de dados pelo seu ID."""
        session = self.Session()
        pergunta = session.query(Pergunta).get(id_pergunta)
        if pergunta:
            session.delete(pergunta)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    def listar_perguntas_por_robo(self, id_robo):
        """Retorna uma lista com todas as perguntas associadas ao robô especificado."""
        session = self.Session()
        perguntas = session.query(Pergunta).filter_by(id_robo=id_robo).all()
        session.close()
        return perguntas
    
    def listar_mensagens_pergunta(self, id_pergunta):
        """Retorna uma lista com todas as mensagens associadas à pergunta especificada."""
        session = self.Session()

        # Obtém a pergunta pelo ID
        pergunta = session.query(Pergunta).get(id_pergunta)

        if not pergunta:
            print("A pergunta não foi encontrada.")
            session.close()
            return []

        # Carrega explicitamente as mensagens associadas à pergunta
        mensagens = pergunta.mensagens

        session.close()

        return mensagens
    
    def adicionar_mensagem_pergunta(self, id_pergunta, mensagem, sequencia_mensagem, id_funcao = None, params_funcao = None):
        """Adiciona uma nova mensagem à pergunta com o ID especificado."""
        session = self.Session()
        pergunta = session.query(Pergunta).get(id_pergunta)
        if pergunta:
            nova_mensagem = MensagemPergunta(id_pergunta=id_pergunta, mensagem=mensagem, sequencia_mensagem=sequencia_mensagem, id_funcao=id_funcao)
            pergunta.mensagens.append(nova_mensagem)
            session.add(nova_mensagem)
            session.commit()
            mensagem_id = nova_mensagem.id
            session.close()
            return mensagem_id
        session.close()
        return None
    
    def listar_mensagens_pergunta(self, id_pergunta):
        """Retorna uma lista com todas as mensagens associadas à pergunta especificada."""
        session = self.Session()

        # Obtém a pergunta pelo ID
        pergunta = session.query(Pergunta).get(id_pergunta)

        if not pergunta:
            print("A pergunta não foi encontrada.")
            session.close()
            return []

        # Carrega explicitamente as mensagens associadas à pergunta
        mensagens = pergunta.mensagens

        session.close()

        return mensagens
    
    def alterar_mensagem_pergunta(self, id_mensagem, mensagem_nova, id_funcao = None, params_funcao = None):
        """Altera a mensagem de uma mensagem associada à pergunta."""
        session = self.Session()
        mensagem = session.query(MensagemPergunta).get(id_mensagem)
        if mensagem:
            mensagem.mensagem = mensagem_nova
            if(id_funcao != None):
                mensagem.id_funcao = id_funcao
            if(params_funcao != None):
                mensagem.params_funcao = params_funcao
            mensagem.last_update = datetime.utcnow()
            session.commit()
            session.close()
            return True
        session.close()
        return False
    
    def excluir_mensagem_pergunta(self, id_mensagem):
        """Exclui uma mensagem associada à pergunta."""
        session = self.Session()
        mensagem = session.query(MensagemPergunta).get(id_mensagem)
        if mensagem:
            session.delete(mensagem)
            session.commit()
            session.close()
            return True
        session.close()
        return False
    
    def excluir_pergunta(self, id_pergunta):
        """Exclui uma pergunta e suas mensagens associadas."""
        session = self.Session()

        # Verifica se a pergunta existe no banco de dados
        pergunta = session.query(Pergunta).get(id_pergunta)
        if not pergunta:
            print("A pergunta não foi encontrada.")
            session.close()
            return False

        # Exclui as mensagens associadas à pergunta
        for mensagem in pergunta.mensagens:
            session.delete(mensagem)

        # Exclui a pergunta
        session.delete(pergunta)

        # Faz o commit das exclusões
        session.commit()
        session.close()

        print("A pergunta e suas mensagens foram excluídas com sucesso.")
        return True
    
    def limpar_tabelas(self, security = False):
        if(security == True):
            return
        """Limpa todas as tabelas (exclui todos os registros)."""
        session = self.Session()

        # Exclui todos os registros da tabela MensagemPergunta
        session.query(MensagemPergunta).delete()

        # Exclui todos os registros da tabela Pergunta
        session.query(Pergunta).delete()

        # Faz o commit das exclusões
        session.commit()
        session.close()

        print("Todas as tabelas foram limpas.")
        
    def obter_ultima_pergunta_por_robo(self, id_robo):
        """Retorna a última pergunta associada ao robô especificado."""
        session = self.Session()

        ultima_pergunta = session.query(Pergunta).filter_by(id_robo=id_robo).order_by(desc(Pergunta.id)).first()

        session.close()

        return ultima_pergunta