from fastapi import APIRouter, Body, status

from workout_api.centro_treinamento.schemas import CtIn, CtOut
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    path="/",
    summary="Criar novo CT",
    status_code=status.HTTP_201_CREATED,
    response_model=CtOut,
)
async def post(
    db_session: DatabaseDependency,
    ct_in: CtIn = Body(...)
) -> CtOut:
    pass
