from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_async_session
from src.paintings.models import PaintingModel
from src.paintings.schemas import PaintingCreate, PaintingOut

router = APIRouter()

def verify_author_token(authorization: str = Header(...)):
    if authorization != "Bearer secret-art-token-2026":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или отсутствующий токен автора"
        )

@router.post("/", dependencies=[Depends(verify_author_token)])
async def create_painting(painting: PaintingCreate, session: AsyncSession = Depends(get_async_session)):
    db_painting = PaintingModel(
        title=painting.title,
        price=painting.price,
        quote=painting.description,
        image_url=painting.image_url
    )
    session.add(db_painting)
    await session.commit()
    await session.refresh(db_painting)
    return {"status": "success"}


@router.get("/", response_model=list[PaintingOut])
async def get_paintings(session: AsyncSession = Depends(get_async_session)):
    query = select(PaintingModel)
    result = await session.execute(query)
    paintings = result.scalars().all()
    formatted_paintings = []
    for p in paintings:
        formatted_paintings.append({
            "id": p.id,
            "title": p.title,
            "price": p.price,
            "image_url": p.image_url,
            "description": p.quote  # Фронтенд получит то, что ожидает
        })
        
    return formatted_paintings


@router.delete("/{painting_id}", dependencies=[Depends(verify_author_token)])
async def delete_painting(painting_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(PaintingModel).where(PaintingModel.id == painting_id)
    result = await session.execute(query)
    painting = result.scalar_one_or_none()
    
    if not painting:
        raise HTTPException(
            status_code=404, 
            detail="Картина не найдена в экспозиции"
        )
        
    await session.delete(painting)
    await session.commit()
    return {"status": "success", "message": "Картина успешно удалена"}