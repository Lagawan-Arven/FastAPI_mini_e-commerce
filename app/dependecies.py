from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from app.database import local_session
from app.database_model import CUSTOMER
from sqlalchemy.orm import Session

from app.auth import SECRET_KEY,ALGORITHM
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_test")

def get_session():
    session = local_session()
    try:
        yield session
    finally:
        session.close()

def get_current_user(token: str =  Depends(oauth2_scheme),
                     session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        customer_id = int(payload.get("id"))
    except:
        raise HTTPException(status_code=400,detail="Invalid token!")
    
    db_user = session.query(CUSTOMER).filter(CUSTOMER.id==customer_id).first()
    if not db_user:
        raise HTTPException(status_code=404,detail="Customer not found!")
    
    return db_user