from pydantic import BaseModel
from typing import Optional, List
from model.serie import Serie



class SerieSchema(BaseModel):
    """ Define como uma nova serie a ser inserido deve ser representado
    """
    id: int = 1
    nome: str = "Friends"
    temporadas: Optional[int] = '10'
    plataforma: str = "HBO MAX"


class SerieBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da Serie.
    """
    id: int = 1


class ListagemSerieSchema(BaseModel):
    """ Define como uma listagem de Series será retornada.
    """
    Series:List[SerieSchema]


def apresenta_Series(Series: List[Serie]):
    """ Retorna uma representação da serie seguindo o schema definido em
        SerieViewSchema.
    """
    result = []
    for Serie in Series:
        result.append({
            "id": Serie.id,
            "nome": Serie.nome,
            "temporadas": Serie.temporadas,
            "plataforma": Serie.plataforma,
        })

    return {"Series": result}


class SerieViewSchema(BaseModel):
    """ Define como uma serie será retornado: Series.
    """
    id: int = 1
    nome: str = "Friends"
    temporadas: Optional[int] = '10'
    plataforma: str = "HBO MAX"


class SerieDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int

def apresenta_Serie(Serie: Serie):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": Serie.id,
        "nome": Serie.nome,
        "temporadas": Serie.temporadas,
        "plataforma": Serie.plataforma
    }
