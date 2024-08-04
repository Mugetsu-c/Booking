from sqlalchemy import select

from App.database import async_session_maker
from App.bookings.models import Bookings
from App.DAO.base import BaseDAO


class BookingDAO(BaseDAO):
    model = Bookings