from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Ema
from .schemas import EmaCreate
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_emas(db: AsyncSession, skip: int = 0, limit: int = 20):
    logger.info(f"Fetching emas with skip={skip}, limit={limit}")
    result = await db.execute(select(Ema).order_by(Ema.created_at.desc()).offset(skip).limit(limit))
    emas = result.scalars().all()
    logger.info(f"Found {len(emas)} emas")
    for ema in emas:
        logger.info(f"Ema: id={ema.id}, name='{ema.name}', message='{ema.message}', type='{ema.type}', created_at={ema.created_at}")
    return emas

async def create_ema(db: AsyncSession, ema_in: EmaCreate):
    logger.info(f"Creating new ema: name='{ema_in.name}', message='{ema_in.message}', type='{ema_in.type}'")
    ema = Ema(**ema_in.dict())
    db.add(ema)
    await db.commit()
    await db.refresh(ema)
    logger.info(f"Created ema with id={ema.id} at {ema.created_at}")
    return ema
