from App.users.models import Users
from App.DAO.base import BaseDAO


class UsersDAO(BaseDAO):
    model = Users