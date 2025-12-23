from contextlib import asynccontextmanager
from sqlalchemy import text
import os
import logging

from app.database import models
from app.database.database import engine,local_session
from app.auth import hash_password

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app):

    #===============================
        #VALIDATE ENVIRONMENT
    #===============================
    required_env = ["DB_USER","DB_PASSWORD","DB_HOST","DB_PORT","DB_NAME","SECRET_KEY","ALGORITHM"]

    for variable in required_env:
        if not os.getenv(variable):
            raise RuntimeError(f"Missing environment variable: {variable}")
        
    #===============================
        #CHECKS DATABASE
    #===============================
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        raise RuntimeError("Database Connection Failed!") from e
    
    #===============================
        #CREATE ADMIN USER
    #===============================
    session = local_session()
    try:
        admin = session.query(models.User).filter(models.User.role=="admin").first()
        if not admin:
            admin = models.User(
                username = "admin",
                email = "admin",
                password = hash_password("1234") ,
                role = "admin",
                fullname = "System Admin",
                age = 0,
                gender = "admin",
                occupation = "admin"
            )
            session.add(admin)
            session.commit()
    finally:
        session.close()

    logger.info("🚀 Application startup")
    yield
    logger.info("🛑 Application shutdown")

    engine.dispose()