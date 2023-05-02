from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Serie(Base):
    __tablename__ = 'Serie'

    id = Column("pk_Serie", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    temporadas = Column(Integer)
    plataforma = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome:str, temporadas:int, plataforma:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Inserir uma Serie

        Arguments:
            nome: nome da Serie.
            temporadas: quantidade temporadas que a serie possue
            pplataforma: plataforma de streming para assistir a serie
            data_insercao: data de quando o produto foi inserido à base
        """
        self.nome = nome
        self.temporadas = temporadas
        self.plataforma = plataforma

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
