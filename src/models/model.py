from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    email = Column("email", String, nullable=False)
    cpf = Column("cpf", String, nullable=False)
    senha = Column("senha", String, nullable=False)
    ativo = Column("ativo", Boolean)

    contas = relationship("Conta", back_populates="usuario")

    def __init__(self, nome, email, cpf, senha, ativo=True):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.senha = senha
        self.ativo = ativo



class Conta(Base):
    __tablename__ = "contas"


    id = Column("id", Integer, primary_key=True, autoincrement=True)
    numero_conta = Column("numero_conta", String, nullable=False, unique=True)
    saldo = Column("saldo", Float, default=0, nullable=True)
    ativo = Column("ativo", Boolean)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="contas")

    data_de_criacao = Column(Date)


    transacoes_enviadas = relationship(
        "Transacao", 
        foreign_keys="[Transacao.conta_de_origem_id]", 
        back_populates="conta_origem"
    )

    transacoes_recebidas = relationship(
        "Transacao", 
        foreign_keys="[Transacao.conta_de_destino_id]", 
        back_populates="conta_destino"
    )

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    
    data_da_transacao = Column(Date)

    conta_de_origem_id = Column(Integer, ForeignKey("contas.id"))
    conta_de_destino_id = Column(Integer, ForeignKey("contas.id"))

    valor = Column(Float)

    def __init__(self, data_da_transacao, conta_de_origem_id: int, conta_de_destino_id: int, valor: float):
        self.data_da_transacao = data_da_transacao
        self.conta_de_origem_id = conta_de_origem_id
        self.conta_de_destino_id = conta_de_destino_id
        self.valor = valor



    conta_origem = relationship(
        "Conta", 
        foreign_keys=[conta_de_origem_id], 
        back_populates="transacoes_enviadas"
    )
    
    conta_destino = relationship(
        "Conta", 
        foreign_keys=[conta_de_destino_id], 
        back_populates="transacoes_recebidas"
    )


