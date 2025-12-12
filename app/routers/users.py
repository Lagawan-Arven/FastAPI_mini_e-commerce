from fastapi import FastAPI,HTTPException,Depends,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database_model import CUSTOMER
from ..dependecies import get_session,get_current_user
from ..models import Customer_Create,Customer_Out,Product_Create,Product_Out
from ..auth import hash_password,verify_password,create_access_token

router = APIRouter()

#===============================
        #REGISTER A USER
#===============================
@router.post("/register")
def register_user(customer: Customer_Create,
                  session: Session = Depends(get_session)):
    
    #Checks if the customer's account already existed
    db_customer = session.query(CUSTOMER).filter(CUSTOMER.username==customer.username).first()
    if db_customer:
        raise HTTPException(status_code=400,detail="Account already existed!")
    
    hashed_password = hash_password(customer.password)
    new_customer = CUSTOMER(
        name = customer.firstname.capitalize() +" "+ customer.lastname.capitalize(),
        age = customer.age,
        sex = customer.sex.capitalize(),
        occupation = customer.occupation.capitalize(),
        username = customer.username,
        password = hashed_password
    )
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    return {"message":"Account successfully registered"}

#===============================
        #LOGI IN USER
#===============================
@router.post("/login")
def login_user(username:str,
               password: str,
               session: Session = Depends(get_session)):
    
    db_customer = session.query(CUSTOMER).filter(CUSTOMER.username==username).first()
    if not db_customer:
        raise HTTPException(status_code=404,detail="Account did not exist!")
    if not verify_password(password,db_customer.password):
        raise HTTPException(status_code=404,detail="Incorrect password!")
    
    token = create_access_token({"id":db_customer.id})

    return {"message":"Log in successful!","access_token":token,"token_type":"bearer"}

@router.post("/login_test")
def login_user(data_form: OAuth2PasswordRequestForm = Depends(),
               session: Session = Depends(get_session)):
    
    db_customer = session.query(CUSTOMER).filter(CUSTOMER.username==data_form.username).first()
    if not db_customer:
        raise HTTPException(status_code=404,detail="Account did not exist!")
    
    if not verify_password(data_form.password,db_customer.password):
        raise HTTPException(status_code=400,detail="Incorrect password!")
    
    token = create_access_token({"id":db_customer.id})

    return {"message":"Log in successful!","access_token":token,"token_type":"bearer"}