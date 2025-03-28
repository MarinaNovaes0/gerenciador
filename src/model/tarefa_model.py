from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, Integer

Base = declarative_base()

class Tarefa(Base):
    __tablename__ = 'tb_tarefas_mine'

    id = Column(Integer, primary_key=True ,autoincrement=True)
    descricao = Column(Text, nullable=True)

    def __init__ (self, descricao):
        self.descricao = descricao


def create_tables(engine):
    Base.metadata.create_all(engine)