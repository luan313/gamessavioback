from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.database.session import get_db
from app.core.security import get_current_user
from app.schemas.jogos_monitorados import MonitoramentoCreate, MonitoramentoUpdate, MonitoramentoResponse 
from app.services import monitoramento_service as crud_monitoramento

router = APIRouter(prefix="/monitoramentos")

@router.post("/", response_model=MonitoramentoResponse, status_code=status.HTTP_201_CREATED)
async def create_new_monitoramento(
    monitoramento: MonitoramentoCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await crud_monitoramento.create_monitoramento(db=db, monitoramento=monitoramento, user_id=current_user.id)


@router.get("/", response_model=List[MonitoramentoResponse])
async def read_monitoramentos(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await crud_monitoramento.get_monitored_games_for_user(db, current_user.id, skip, limit)


@router.patch("/{monitoramento_id}", response_model=MonitoramentoResponse)
async def update_existing_monitoramento(
    monitoramento_id: UUID,
    monitoramento: MonitoramentoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated_monitoramento = await crud_monitoramento.update_monitoring(
        db, monitoramento_id, monitoramento, current_user.id
    )

    if updated_monitoramento == "unauthorized":
        raise HTTPException(status_code=403, detail="Não autorizado a editar este monitoramento")
    
    if not updated_monitoramento:
        raise HTTPException(status_code=404, detail="Monitoramento não encontrado")
        
    return updated_monitoramento


@router.delete("/{monitoramento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_monitoramento(
    monitoramento_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = await crud_monitoramento.delete_monitoramento(db, monitoramento_id, current_user.id)

    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="Não autorizado a remover este monitoramento")
    
    if not result:
        raise HTTPException(status_code=404, detail="Monitoramento não encontrado")
    
    return None