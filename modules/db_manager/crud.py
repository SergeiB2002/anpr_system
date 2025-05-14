import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import vehicles, blacklist, access_rules, recognition_events

db_url = getenv('DATABASE_URL')
engine = create_async_engine(db_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def validate_format(plate: str) -> bool:
    async with AsyncSessionLocal() as sess:
        q = await sess.execute(sa.select(vehicles).where(vehicles.c.plate==plate))
        return q.scalars().first() is not None

async def verify_plate(plate: str) -> str:
    async with AsyncSessionLocal() as sess:
        bl = await sess.execute(sa.select(blacklist).where(blacklist.c.plate==plate))
        if bl.scalars().first():
            status = 'INVALID'
        else:
            ar = await sess.execute(sa.select(access_rules).where(access_rules.c.plate==plate))
            row = ar.scalars().first()
            status = 'VALID' if row and row.allowed else 'INVALID'
        # логируем
        await sess.execute(recognition_events.insert().values(id=str(uuid4()), plate=plate, ts=sa.func.now(), status=status))
        await sess.commit()
        return status