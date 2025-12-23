from fastapi import HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session

from app.database import models
from app.dependecies import get_session,get_current_user
from app import schemas

router = APIRouter()

#===============================
        #GET ALL PRODUCTS
#===============================
@router.get("/products",response_model=list[schemas.User_Product_Out])
def get_all_products(limit: int = 10, offset: int = 0,
                    user = Depends(get_current_user),
                    session: Session = Depends(get_session)):

    current_user = session.get(models.User,user.id)
    if not current_user:
        raise HTTPException(status_code=401,detail="User not logged in!")
    
    db_products = session.query(models.Product).all()
    if not db_products:
        raise HTTPException(status_code=404,detail="There is no products yet")
    
    return db_products