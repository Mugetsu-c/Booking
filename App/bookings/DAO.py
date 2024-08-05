from App.bookings.models import Bookings
from App.DAO.base import BaseDAO


class BookingDAO(BaseDAO):
    model = Bookings