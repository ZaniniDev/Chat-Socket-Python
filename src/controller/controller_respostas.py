from sqlalchemy import create_engine, Column, Integer, String, MetaData, DateTime, desc, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta

Base = declarative_base()

class Resposta(Base):
    __tablename__ = 'respostas_robos'
    # Obtém o datetime atual em UTC
    datetime_utc = datetime.utcnow()
    # Subtrai 3 horas do horario (HORARIO BRASILEIRO)
    datetime_brasil = datetime_utc - timedelta(hours=3)
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_pergunta = Column(Integer)
    tipo_resposta = Column(String)
    resposta = Column(String)
    opcao = Column(String, default=None)
    variavel = Column(String, default=None)
    tipo_variavel = Column(String, default=None)
    confirmacao_variavel = Column(Integer, default=0)
    id_proxima_pergunta = Column(Integer, default=None)
    dt_create = Column(DateTime, default=datetime_brasil)
    last_update = Column(DateTime, default=datetime_brasil, onupdate=datetime_brasil) 


    def __init__(self, id_pergunta, tipo_resposta, resposta, id_proxima_pergunta = None, opcao=None, variavel=None, tipo_variavel=None, confirmacao_variavel = 0):
        self.id_pergunta = id_pergunta
        self.tipo_resposta = tipo_resposta
        self.resposta = resposta
        self.opcao = opcao
        self.variavel = variavel
        self.id_proxima_pergunta = id_proxima_pergunta
        self.tipo_variavel = tipo_variavel
        self.confirmacao_variavel = confirmacao_variavel
       
class RespostasController:
    def __init__(self, caminhobd):
        self.caminhobd = caminhobd
        # Conecta ao banco de dados SQLite
        self.engine = create_engine(f'sqlite:///{caminhobd}')
        # Cria as tabelas no banco de dados (caso ainda não existam)
        Base.metadata.create_all(self.engine)
        # Cria uma fábrica de sessão para interagir com o banco de dados
        self.Session = sessionmaker(bind=self.engine)

    def cadastrar_resposta(self, id_pergunta, tipo_resposta, resposta, id_proxima_pergunta = None, opcao=None, variavel=None, tipo_variavel=None):
        """Cadastra uma nova resposta no banco de dados."""
        print("Cadastrar nova resposta")
        
        new_resposta = Resposta(id_pergunta=id_pergunta, tipo_resposta=tipo_resposta,
                                resposta=resposta, opcao=opcao, variavel=variavel, id_proxima_pergunta=id_proxima_pergunta, tipo_variavel=tipo_variavel)
        session = self.Session()
        session.add(new_resposta)
        session.commit()
        id_resposta = new_resposta.id
        session.close()
        return id_resposta

    def atualizar_resposta(self, id_resposta, tipo_resposta = None, resposta = None, id_proxima_pergunta = None, opcao=None, variavel=None):
        """Atualiza os dados de uma resposta existente no banco de dados."""
        session = self.Session()
        resposta_atualizada = session.query(Resposta).filter_by(id=id_resposta).first()
        if resposta_atualizada:
            if(tipo_resposta != None):
                resposta_atualizada.tipo_resposta = tipo_resposta
            if(resposta != None):
                resposta_atualizada.resposta = resposta
            if(opcao != None):
                resposta_atualizada.opcao = opcao
            if(variavel != None):
                resposta_atualizada.variavel = variavel
            if(id_proxima_pergunta != None):
                resposta_atualizada.id_proxima_pergunta = id_proxima_pergunta
            session.commit()
            session.close()
            return True
        else:
            session.close()
            return False

    def remover_resposta(self, id_resposta):
        """Remove uma resposta do banco de dados."""
        session = self.Session()
        resposta_removida = session.query(Resposta).filter_by(id=id_resposta).first()
        if resposta_removida:
            session.delete(resposta_removida)
            session.commit()
            session.close()
            return True
        else:
            session.close()
            return False

    def obter_resposta_por_id(self, id_resposta):
        """Obtém os detalhes de uma resposta do banco de dados."""
        session = self.Session()
        resposta = session.query(Resposta).filter_by(id=id_resposta).first()
        session.close()
        return resposta

    def listar_respostas_por_pergunta(self, id_pergunta):
        """Lista as respostas associadas a uma pergunta específica do banco de dados."""
        session = self.Session()
        respostas = session.query(Resposta).filter_by(id_pergunta=id_pergunta).all()
        session.close()
        return respostas 
    
    def existe_resposta_pergunta(self, id_pergunta):
        session = self.Session()
        respostas = session.query(Resposta).filter_by(id_pergunta=id_pergunta).all()
        session.close()
        existe_resposta = True if len(respostas) > 0 else False
        return existe_resposta 

    def limpar_tabelas(self, security = False):
        if(security == True):
            return
        """Limpa todas as tabelas (exclui todos os registros)."""
        session = self.Session()

        # Exclui todos os registros da tabela Respostas
        session.query(Resposta).delete()

        # Faz o commit das exclusões
        session.commit()
        session.close()

        print("Todas as tabelas foram limpas.")
    
