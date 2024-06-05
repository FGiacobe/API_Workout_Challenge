from datetime import datetime, timezone
from typing import List
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from workout_api import atleta
from workout_api.centro_treinamento.models import CentrosTreinamentoModel
from workout_api.categorias.models import CategoriasModel
from workout_api.atleta.models import AtletasModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    path="/",
    summary="Criar novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):

    nome_categoria = atleta_in.categoria.nome
    nome_ct = atleta_in.ct_atleta.nome

    categoria = (
        (
            await db_session.execute(
                select(CategoriasModel).filter_by(nome=nome_categoria)
            )
        )
        .scalars()
        .first()
    )
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A categoria {nome_categoria} não foi encontrada.",
        )

    ct = (
        (
            await db_session.execute(
                select(CentrosTreinamentoModel).filter_by(nome=nome_ct)
            )
        )
        .scalars()
        .first()
    )

    if not ct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O CT {nome_ct} não foi encontrado.",
        )

    try:
        atleta_out = AtletaOut(
            id=uuid4(), created_at=datetime.now(timezone.utc), **atleta_in.model_dump()
        )
        atleta_model = AtletasModel(
            **atleta_out.model_dump(exclude={"categoria", "ct"})
        )
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = ct.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except Exception as err:
        # breakpoint()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao inserir os dados no banco. Erro: {err}",
        )

    return atleta_out


@router.get(
    path="/",
    summary="Consultar todos os atletas",
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut],
)
async def query(db_session: DatabaseDependency) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (
        (await db_session.execute(select(AtletasModel))).scalars().all()
    )
    return atletas


@router.get(
    path=f"/{id}",
    summary="Consultar atleta por id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query_id(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletasModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not atleta:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no id: {id}",
        )

    return atleta
