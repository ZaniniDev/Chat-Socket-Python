from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    # Obtém o datetime atual em UTC
    datetime_utc = datetime.utcnow()
    # Subtrai 3 horas do horario (HORARIO BRASILEIRO)
    datetime_brasil = datetime_utc - timedelta(hours=3)
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    apelido = Column(String)
    celularprincipal = Column(String)
    celular = Column(String)
    keyacesso = Column(String)
    ativado = Column(Boolean, default=True)
    dt_create = Column(DateTime, default=datetime_brasil)
    last_update = Column(DateTime, default=datetime_brasil, onupdate=datetime_brasil)   

class UsuarioController:
    def __init__(self, caminho_banco_dados):
        engine = create_engine(f'sqlite:///{caminho_banco_dados}')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def cadastrar_usuario(self, nome, apelido, celularprincipal, keyacesso, ativado=True):
        usuario = Usuario(nome=nome, apelido=apelido, celularprincipal=celularprincipal, keyacesso=keyacesso, ativado=ativado)
        self.session.add(usuario)
        self.session.commit()
        return usuario.id

    def listar_usuarios(self):
        return self.session.query(Usuario).all()

    def buscar_usuario_por_id(self, id_usuario):
        return self.session.query(Usuario).get(id_usuario)

    def atualizar_usuario(self, id_usuario, nome=None, apelido=None, celularprincipal=None, keyacesso=None, ativado=None):
        usuario = self.session.query(Usuario).get(id_usuario)
        if not usuario:
            return False

        if nome is not None:
            usuario.nome = nome
        if apelido is not None:
            usuario.apelido = apelido
        if celularprincipal is not None:
            usuario.celularprincipal = celularprincipal
        if keyacesso is not None:
            usuario.keyacesso = keyacesso
        if ativado is not None:
            usuario.ativado = ativado

        self.session.commit()
        return True

    def excluir_usuario(self, id_usuario):
        usuario = self.session.query(Usuario).get(id_usuario)
        if not usuario:
            return False

        self.session.delete(usuario)
        self.session.commit()
        return True

    def fechar_conexao(self):
        self.session.close()