from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from App.database import engine, SessionLocal
from App.database import Base
from App.models import User,Documents,Versions
from App.routers import User,Documents

Base.metadata.create_all(bind=engine)
app = FastAPI()

templates = Jinja2Templates(directory="App/templates")
app.mount("/static", StaticFiles(directory="App/static"), name="static")

app.include_router(User.router)
app.include_router(Documents.router)

@app.get("/")
def home():
    return RedirectResponse(url="/auth/")

