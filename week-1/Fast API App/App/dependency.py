from fastapi import HTTPException, Cookie, status
from fastapi.responses import RedirectResponse
from jose import jwt, JWTError
from App.core.security import SECRET_KEY, ALGORITHM

def get_current_user(access_token: str | None = Cookie(default=None)):
    if not access_token:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user_id

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

