from fastapi import APIRouter, Depends, HTTPException, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from App.database import get_db
from App.models.User import User
from App.schemas.user import UserCreate,Userlogin
from App.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authorization"])
templates = Jinja2Templates(directory="App/templates")

@router.get("/")
def get_user_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

#User creation(signup)
@router.post("/register")
def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter(User.Username == username).first():
        raise HTTPException(status_code=400, detail="User already registered")

    new_user = User(
        Username=username,
        Hashed_password=hash_password(password)
    )
    db.add(new_user)
    db.commit()
    return {'message': 'User registered successfully'}

#Userlogin and token giving
@router.post("/login")
def login(request:OAuth2PasswordRequestForm=Depends() , db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.Username == request.username).first()

    if not db_user or not verify_password(request.password, db_user.Hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    response = RedirectResponse(url="/documents/", status_code=status.HTTP_302_FOUND)

    # store token in cookie
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/auth")
    response.delete_cookie("access_token")
    return response
