from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Ema
from .schemas import EmaCreate
import logging
from sqlalchemy import text

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Banned words list
BANNED_WORDS = [
    'nigger', 'nigga', 'fuck', 'shit', 'bitch', 'cunt', 'dick', 'pussy', 'asshole',
    'motherfucker', 'fucker', 'whore', 'slut', 'bastard', 'damn', 'hell'
]

def contains_banned_words(text):
    """Check if text contains any banned words (case insensitive)."""
    if not text:
        return False
    text_lower = text.lower()
    return any(word in text_lower for word in BANNED_WORDS)

async def clean_banned_content(db: AsyncSession):
    """Remove any existing emas that contain banned words."""
    logger.info("Cleaning banned content from database")
    result = await db.execute(text("SELECT id, message FROM emas"))
    emas = result.fetchall()
    
    deleted_count = 0
    for ema in emas:
        if contains_banned_words(ema.message):
            await db.execute(text("DELETE FROM emas WHERE id = ?"), (ema.id,))
            deleted_count += 1
            logger.info(f"Deleted ema {ema.id} containing banned content")
    
    if deleted_count > 0:
        await db.commit()
        logger.info(f"Deleted {deleted_count} emas with banned content")
    
    return deleted_count

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
    
    # Check for banned words
    if contains_banned_words(ema_in.message):
        logger.warning(f"Rejected ema with banned content: {ema_in.message}")
        raise ValueError("Message contains inappropriate content")
    
    ema = Ema(**ema_in.dict())
    db.add(ema)
    await db.commit()
    await db.refresh(ema)
    logger.info(f"Created ema with id={ema.id} at {ema.created_at}")
    return ema

async def delete_all_emas(db: AsyncSession):
    logger.info("Deleting all emas from the database")
    await db.execute(text("DELETE FROM emas"))
    await db.commit()
    logger.info("All emas deleted.")
