from fastapi import APIRouter
from sqlalchemy import select

from App.database import async_session_maker
from App.bookings.models import Bookings


router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
async def get_bookings():
    async with async_session_maker() as session:
        query = select(Bookings)
        result = await session.execute(query)
        return result.mappings().all()

@router.get('/{booking_id}')
async def get_bookings(booking_id: int = None):
    async with async_session_maker() as session:
        query = select(Bookings).where(Bookings.id == booking_id)
        result = await session.execute(query)
        return result.mappings().all()