from contextlib import asynccontextmanager
from sqlalchemy import text
import os
import logging

from app.database import models
from app.database.database import engine,local_session
from app.core.auth import hash_password
from app.database.database import init_db
from app. database.wait_for_db import wait_for_db

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app):

    #===============================
        #VALIDATE ENVIRONMENT
    #===============================
    required_env = ["DB_URL","SECRET_KEY","ALGORITHM"]

    for variable in required_env:
        if not os.getenv(variable):
            raise RuntimeError(f"Missing environment variable: {variable}")
        
    #===============================
        #WAIT FOR DATABASE
    #===============================
    wait_for_db(engine, max_retries=10, delay_seconds=2)
   
   #===============================
        #INITIALIZE DATABASE
    #===============================
    if os.getenv("TESTING") == "1":
        logger.info("⚠️ Running in TESTING mode")
    else:
        init_db()

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

    logger.info("🚀 Application startup complete")

    yield
    
    logger.info("🛑 Application shutdown")

    engine.dispose()