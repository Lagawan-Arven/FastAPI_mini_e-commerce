from fastapi import FastAPI
from app.routers.login import router as users_router
from app.routers.products import router as products_router

app = FastAPI()

app.include_router(users_router)
app.include_router(products_router)