from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.models.users import User, GetUserById
from sqlmodel import Session
from app.db.session import get_session
from dotenv import load_dotenv
from jose import JWTError, jwt  

import os

load_dotenv()

security = HTTPBearer()
JWT_SECRET = os.getenv("JWT_SECRET")
print(JWT_SECRET)
ALGORITHM = "HS256"

def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    token = credentials.credentials
    try:
        print("TOKEN DITERIMA:", token)
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        print("PAYLOAD BERHASIL:", payload)

        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token tidak mengandung user ID"
            )

        user = GetUserById(user_id, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User tidak ditemukan"
            )

        return user

    except JWTError as e:
        print("JWT ERROR:", str(e))
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token tidak valid atau telah kadaluarsa"
        )
