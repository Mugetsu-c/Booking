from fastapi import APIRouter, HTTPException, status, Response, Depends
from App.users.auth import get_password_hash, verify_password, authenticate_user, create_password_token
from App.users.schemas import SUserAuth
from App.users.DAO import UsersDAO
from App.users.dependencies import get_current_user
from App.users.models import Users


router = APIRouter(
    prefix='/auth',
    tags=['Auth & Users'],
)


@router.get('')
async def get_users():
    result = await UsersDAO.find_all()
    return result

@router.get('/me') # Получение информации о текущем пользователе
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user




@router.post('/register') # Регистрация нового пользователя
async def register_user(user: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user.email)
    if existing_user:
        raise HTTPException(status_code=500, detail='Email already registered')
    hashed_password = get_password_hash(user.password)
    await UsersDAO.add(email=user.email, hashed_password=hashed_password)


@router.post('/login') #Авторизация пользователя
async def login_user(
    response: Response,
    user: SUserAuth):
    user = await authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(stasus_code=status.HTTP_401_UNAUTHORIZED)
    
    access_token = create_password_token({'sub': str(user.id)})
    response.set_cookie(key='booking_access_token', value=access_token, httponly=True)
    return access_token

@router.post('/logout') # Выход из системы
async def logout_user(response: Response):
    response.delete_cookie(key='booking_access_token')

