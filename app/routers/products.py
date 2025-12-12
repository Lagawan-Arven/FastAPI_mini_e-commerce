from fastapi import FastAPI,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database_model import CUSTOMER,PRODUCT
from ..dependecies import get_session,get_current_user
from ..models import Product_Create,Product_Out

router = APIRouter()

@router.post("/products")
def add_prodcuct(product_input: Product_Create,
                 current_user = Depends(get_current_user),
                 session: Session = Depends(get_session)):
    
    db_customer = session.query(CUSTOMER).filter(CUSTOMER.id==current_user.id).first()
    if not db_customer:
        return {"message":"Not logged in!"}
    
    new_product = PRODUCT(
        name = product_input.name,
        price = product_input.price,
        user_id = db_customer.id
    )
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return {"message":"Product added successfully!"}

@router.get("/products",response_model=list[Product_Out])
def get_all_products(current_user = Depends(get_current_user),
                     session: Session = Depends(get_session)):

    db_customer = session.query(CUSTOMER).filter(CUSTOMER.id==current_user.id).first()
    if not db_customer:
        return {"message":"Not logged in!"}
    
    db_products = session.query(PRODUCT).filter(PRODUCT.user_id==current_user.id).all()
    if db_products == []:
        raise HTTPException(status_code=400,detail="There is no products yet")
    
    return db_products