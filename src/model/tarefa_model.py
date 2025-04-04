from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, Integer, Boolean, Date

Base = declarative_base()

class Tarefa(Base):
    __tablename__ = 'tb_tarefas_mine'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(Text, nullable=True)
    vencimento = Column(Boolean, nullable=False, default=False)  # Nova coluna
    dt = Column(Date, nullable=True)  # Nova coluna

    def __init__(self, descricao, vencimento=False, dt=None):
        self.descricao = descricao
        self.vencimento = vencimento
        self.dt = dt


def create_tables(engine):
    Base.metadata.create_all(engine)