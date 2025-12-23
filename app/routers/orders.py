from fastapi import HTTPException,APIRouter,Depends
from sqlalchemy.orm import Session

from app import schemas
from app.dependecies import get_current_user,get_session
from app.database import models

router = APIRouter()

#===============================
        #GET ALL ORDERS
#==============================
@router.get("/orders",response_model=list[schemas.Base_Order_Out])
def get_all_orders( user = Depends(get_current_user),
               session: Session = Depends(get_session)):
    
    current_user = session.get(models.User,user.id)
    if not current_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_orders = session.query(models.Order).filter(models.Order.user_id==current_user.id).all()
    if not db_orders:
        raise HTTPException(status_code=404,detail="There is no order yet!")
    
    return db_orders

#===============================
            #ADD ORDER
#===============================
@router.post("/orders",response_model=schemas.Base_Order_Out)
def add_order(order_input: schemas.Base_Order_Create,
              user = Depends(get_current_user),
              session: Session = Depends(get_session)):
    
    try:
        current_user = session.get(models.User,user.id)
        if not current_user:
            raise HTTPException(status_code=401,detail="User not logged in!")
        
        db_product = session.get(models.Product,order_input.product_id)
        if not db_product:
            raise HTTPException(status_code=404,detail="Product not found!")
        
        if db_product.stock < order_input.product_quantity:
            raise HTTPException(status_code=400,detail="Insufficient product stock!")

        new_order = models.Order(
            user_id = current_user.id,
            payment_method = order_input.payment_method,
            payment_status = order_input.payment_status
        )
        new_order.order_products =[ models.Order_Product(
            product_id = db_product.id,
            quantity = order_input.product_quantity
        )]

        db_product.stock -= order_input.product_quantity

        session.add(new_order)
        session.commit()
        session.refresh(new_order)
        return new_order
    
    except HTTPException:
        session.rollback()
        raise

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500,detail="Checkout failed") from e
