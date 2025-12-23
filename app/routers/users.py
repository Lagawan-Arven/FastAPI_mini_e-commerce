from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.dependecies import get_current_user,get_session
from app.database import models
from app import schemas

router = APIRouter()

#===============================
        #GET CURRENT USER
#===============================
@router.get("/user",response_model=schemas.Base_User_Out)
def get_current_user(user = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    
    current_user = session.get(models.User,user.id)
    if not current_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    return current_user

