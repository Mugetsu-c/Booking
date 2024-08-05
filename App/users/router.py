from fastapi import APIRouter, HTTPException
from App.users.auth import get_password_hash, verify_password
from App.users.schemas import SUserAuth
from App.users.DAO import UsersDAO


router = APIRouter(
    prefix='/auth',
    tags=['Auth & Users'],
)


@router.get('')
async def get_users():
    result = await UsersDAO.find_all()
    return result

@router.post('/register')
async def register_user(user: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user.email)
    if existing_user:
        raise HTTPException(status_code=500, detail='Email already registered')
    hashed_password = get_password_hash(user.password)
    await UsersDAO.add(email=user.email, hashed_password=hashed_password)


@router.post('/login')
async def login_user(user: SUserAuth):
    user = await authenticate_user(user.email, user.password)
    