from fastapi import APIRouter
from App.bookings.DAO import BookingDAO
from App.bookings.schemas import SBooking


router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
async def get_bookings() -> list[SBooking]:
    result = await BookingDAO.find_all()
    return result



@router.get('/{booking_id}')
async def get_bookings(booking_id: int):
    result = await BookingDAO.find_by_id(booking_id)
    return result