from fastapi import FastAPI
from app.api.api_v1.endpoints import auth
from app.dependencias import engine
from app.models import Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

app.route("/home")
def home():
    return {"detail": "Welcome to home page"}