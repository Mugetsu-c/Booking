from fastapi import APIRouter, HTTPException, status, Response
from App.users.auth import get_password_hash, verify_password, authenticate_user, create_password_token
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
async def login_user(
    response: Response,
    user: SUserAuth):
    user = await authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(stasus_code=status.HTTP_401_UNAUTHORIZED)
    
    access_token = create_password_token({'sub': user.id})
    response.set_cookie(key='booking_access_token', value=access_token, httponly=True)
    return access_token