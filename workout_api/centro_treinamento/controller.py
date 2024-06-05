from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy import select

from workout_api.centro_treinamento.models import CentrosTreinamentoModel
from workout_api.centro_treinamento.schemas import CtIn, CtOut
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    path="/",
    summary="Criar novo CT",
    status_code=status.HTTP_201_CREATED,
    response_model=CtOut,
)
async def post(db_session: DatabaseDependency, ct_in: CtIn = Body(...)) -> CtOut:
    ct_out = CtOut(id=uuid4(), **ct_in.model_dump())
    ct_model = CentrosTreinamentoModel(**ct_out.model_dump())

    db_session.add(ct_model)
    await db_session.commit()

    return ct_out


@router.get(
    path="/",
    summary="Consultar todas os CTs",
    status_code=status.HTTP_200_OK,
    response_model=list[CtOut],
)
async def query(db_session: DatabaseDependency) -> list[CtOut]:
    ct_list: list[CtOut] = (
        (await db_session.execute(select(CentrosTreinamentoModel))).scalars().all()
    )
    return ct_list


@router.get(
    path=f"/{id}",
    summary="Consultar CT por id",
    status_code=status.HTTP_200_OK,
    response_model=CtOut,
)
async def query_id(id: UUID4, db_session: DatabaseDependency) -> CtOut:
    ct_selected: CtOut = (
        (await db_session.execute(select(CentrosTreinamentoModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not ct_selected:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CT não encontrado no id: {id}",
        )

    return ct_selected
