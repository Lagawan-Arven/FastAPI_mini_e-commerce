from fastapi import FastAPI
from app.database import engine
import database_model
from routers import users,products

app = FastAPI()

database_model.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(products.router)