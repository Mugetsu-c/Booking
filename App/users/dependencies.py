from datetime import datetime
from fastapi import HTTPException, Request, Depends, status
from jose import jwt, JWTError

from App.config import settings
from App.users.DAO import UsersDAO

def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Missing access token'
        )
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITHM_KEY
        )
    except JWTError:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid access token'
        )
    
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Access token expired'
        )

    user_id: str = payload.get('sub')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid user ID'
        )

    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found'
        )
    
    return user