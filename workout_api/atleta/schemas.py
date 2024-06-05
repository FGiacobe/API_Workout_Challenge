# Os schemas são responsáveis pelas validações e serializar os dados
# que apareceram no arquivo json de retorno da API.

from typing import Annotated
from pydantic import Field, PositiveFloat

from workout_api.centro_treinamento.schemas import CtAtleta
from workout_api.categorias.schemas import CategoriaIn
from workout_api.contrib.schemas import BaseSchema, OutMixin


class Atleta(BaseSchema):
    nome: Annotated[
        str, Field(description="Nome do atleta", examples=["João"], max_length=50)
    ]
    cpf: Annotated[
        str, Field(description="CPF do atleta", examples=["12345678900"], max_length=11)
    ]
    idade: Annotated[int, Field(description="Idade do atleta", examples=[25])]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", examples=[75.5])]
    altura: Annotated[
        PositiveFloat, Field(description="Altura do atleta", examples=[1.75])
    ]
    sexo: Annotated[
        str, Field(description="Sexo do atleta", examples=["M"], max_length=1)
    ]
    categoria: Annotated[CategoriaIn, Field(description="Categoria do atleta")]
    ct_atleta: Annotated[CtAtleta, Field(description="CT do atleta")]


class AtletaIn(Atleta):
    pass


class AtletaOut(Atleta, OutMixin):
    pass
