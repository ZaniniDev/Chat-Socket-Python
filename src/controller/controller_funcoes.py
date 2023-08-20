from sqlalchemy import create_engine, Column, Integer, String, MetaData, DateTime, desc, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta

Base = declarative_base()

class Funcoes(Base):
    __tablename__ = 'funcoes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_robo = Column(Integer)
    nome = Column(String)
    descricao = Column(String)
    key_backend = Column(String)

    def __init__(self, id_robo, nome, key_backend, descricao=None):
        self.id_robo = id_robo
        self.nome = nome
        self.key_backend = key_backend
        self.descricao = descricao
       
class FuncoesController:
    def __init__(self, caminhobd):
        self.caminhobd = caminhobd
        # Conecta ao banco de dados SQLite
        self.engine = create_engine(f'sqlite:///{caminhobd}')
        # Cria as tabelas no banco de dados (caso ainda não existam)
        Base.metadata.create_all(self.engine)
        # Cria uma fábrica de sessão para interagir com o banco de dados
        self.Session = sessionmaker(bind=self.engine)

    def obter_key_backend_via_id(self, id_funcao):
        """Obtém as informações do backend da função."""
        session = self.Session()
        funcao = session.query(Funcoes).filter_by(id=id_funcao).first()
        key_backend = ""
        if(funcao != None):
            key_backend = funcao.key_backend
        session.close()
        return key_backend
    