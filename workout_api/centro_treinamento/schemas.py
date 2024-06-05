from typing import Annotated

from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema


class CentroTreinamento(BaseSchema):
    nome: Annotated[
        str,
        Field(
            description="Nome do centro de treinamento",
            examples=["CT King"],
            max_length=20,
        ),
    ]
    endereco: Annotated[
        str,
        Field(
            description="Endereço do centro de treinamento",
            examples=["Av. Mafra, 8356"],
            max_length=60,
        ),
    ]
    proprietario: Annotated[
        str,
        Field(
            description="Proprietário do centro de treinamento",
            examples=["Giacobe"],
            max_length=30,
        ),
    ]


class CtAtleta(BaseSchema):
    nome: Annotated[
        str, Field(description="Nome do CT", examples=["CT King"], max_length=20)
    ]


class CtIn(CentroTreinamento):
    pass


class CtOut(CentroTreinamento):
    id: Annotated[UUID4, Field(description='Identificador do CT')]
