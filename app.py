from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect


from model import Session, Serie
from schemas import *


info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")
series_tag = Tag(name="Series", description="Adição, visualização e remoção de series à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela do estilo de documentação SWAGGER.
    """
    return redirect('/openapi/swagger')


@app.post('/Serie', tags=[series_tag],
          responses={"200": SerieViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_Series(form: SerieSchema):
    """Adiciona uma nova Serie à base de dados

    Retorna uma representação das series e comentários associados.
    """
    serie = Serie(
        nome=form.nome,
        temporadas=form.temporadas,
        plataforma=form.plataforma)

    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(serie)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_Serie(serie), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Essa Serie já foi adicionada na base"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400


@app.get('/Series', tags=[series_tag],
         responses={"200": ListagemSerieSchema, "404": ErrorSchema})
def get_series():
    """Faz a busca por todos as Series cadastrados

    Retorna uma representação da listagem de series.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    series = session.query(Serie).all()

    if not series:
        # se não há series cadastrados
        return {"Series": []}, 200
    else:
        # retorna a representação da serie
        print(series)
        return apresenta_Series(series), 200


@app.get('/Serie', tags=[series_tag],
         responses={"200": SerieViewSchema, "404": ErrorSchema})
def get_serie(query: SerieBuscaSchema):
    """Faz a busca por uma Serie a partir do id da serie

    Retorna uma representação das series e comentários associados.
    """
    serie_id = query.id
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    achou = session.query(Serie).filter(Serie.id == serie_id).first()

    if not achou:
        # se a serie não foi encontrado
        error_msg = "Não foi possivel encontrar essa serie na base"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de serie
        return apresenta_Serie(achou), 200


@app.delete('/Serie', tags=[series_tag],
            responses={"200": SerieDelSchema, "404": ErrorSchema})
def del_Serie(query: SerieBuscaSchema):
    """Deleta uma serie já assistida a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    Series_id = query.id
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Serie).filter(Serie.id == Series_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Serie removida com sucesso", "id": Series_id}
    else:
        # se o produto não foi encontrado
        error_msg = "Não foi possivel encontrar essa serie na base"
        return {"mesage": error_msg}, 404

