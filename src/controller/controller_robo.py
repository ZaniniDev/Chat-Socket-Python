from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()

class Robo(Base):
    __tablename__ = 'robos'
    # Obtém o datetime atual em UTC
    datetime_utc = datetime.utcnow()
    # Subtrai 3 horas do horario (HORARIO BRASILEIRO)
    datetime_brasil = datetime_utc - timedelta(hours=3)

    id = Column(Integer, primary_key=True)
    usuario_criador = Column(Integer)
    nome = Column(String, nullable=False)
    celular = Column(String)
    ativado = Column(Boolean, default=True)    
    keyacesso = Column(String)
    dt_create = Column(DateTime, default=datetime_brasil)
    last_update = Column(DateTime, default=datetime_brasil, onupdate=datetime_brasil)   

class RoboController:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def criar_robo(self, nome, celular=None, ativado=True, keyacesso=None, usuario_criador=None):
        robo = Robo(
            usuario_criador=usuario_criador,
            nome=nome,
            celular=celular,
            ativado=ativado,
            keyacesso=keyacesso
        )
        self.session.add(robo)
        self.session.commit()

    def atualizar_robo(self, robo_id, nome=None, celular=None, ativado=None, keyacesso=None):
        robo = self.session.query(Robo).get(robo_id)
        if robo:
            if nome:
                robo.nome = nome
            if celular:
                robo.celular = celular
            if ativado is not None:
                robo.ativado = ativado
            if keyacesso:
                robo.keyacesso = keyacesso
            robo.last_update = datetime.utcnow()
            self.session.commit()

    def consultar_robo(self, robo_id):
        robo = self.session.query(Robo).get(robo_id)
        return robo

    def excluir_robo(self, robo_id):
        robo = self.session.query(Robo).get(robo_id)
        if robo:
            self.session.delete(robo)
            self.session.commit()