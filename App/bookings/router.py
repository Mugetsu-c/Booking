from fastapi import APIRouter, Request, Depends

from App.bookings.DAO import BookingDAO
from App.bookings.schemas import SBooking
from App.users.models import Users
from App.users.dependencies import get_current_user


router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)): #-> list[SBooking]:
    result = await BookingDAO.find_all(user_id=user.id)
    return result
