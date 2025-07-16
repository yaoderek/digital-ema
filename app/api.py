from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from . import crud, schemas
from .database import SessionLocal
import logging

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/emas", tags=["emas"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=List[schemas.EmaRead])
async def list_emas(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    logger.info(f"GET /api/emas requested with skip={skip}, limit={limit}")
    emas = await crud.get_emas(db, skip=skip, limit=limit)
    logger.info(f"Returning {len(emas)} emas from GET /api/emas")
    return emas

@router.post("/", response_model=schemas.EmaRead, status_code=status.HTTP_201_CREATED)
async def create_ema(ema: schemas.EmaCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"POST /api/emas requested with data: {ema.dict()}")
    try:
        created_ema = await crud.create_ema(db, ema)
        logger.info(f"Returning created ema: {created_ema.id}")
        return created_ema
    except ValueError as e:
        logger.warning(f"Content filtering rejected ema: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/all", status_code=204)
async def delete_all_emas(db: AsyncSession = Depends(get_db)):
    logger.info("DELETE /api/emas/all requested - deleting all emas")
    await crud.delete_all_emas(db)
    return

@router.post("/clean-banned", status_code=200)
async def clean_banned_content(db: AsyncSession = Depends(get_db)):
    logger.info("POST /api/emas/clean-banned requested - cleaning banned content")
    deleted_count = await crud.clean_banned_content(db)
    return {"message": f"Cleaned {deleted_count} emas with banned content", "deleted_count": deleted_count}
