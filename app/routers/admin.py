from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session

from app.dependecies import admin_access,get_session
from app.database import models
from app import schemas

router = APIRouter()

#======================================================================
                            #USERS
#======================================================================
#===============================
        #GET ALL USERS
#===============================
@router.get("/users",response_model=list[schemas.Base_User_Out])
def get_all_users(admin = Depends(admin_access),
                  session: Session = Depends(get_session)):

    current_user = session.get(models.User,admin.id)
    if not current_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_users = session.query(models.User).all()
    if not db_users:
        raise HTTPException(status_code=404,detail="There is no users yet!")
    
    return db_users

#===============================
        #GET USER BY ID
#===============================
@router.get("/user/{user_id}",response_model=schemas.Base_User_Out)
def get_user_by_id(user_id: int, admin = Depends(admin_access),
                   session: Session = Depends(get_session)):
    
    current_user = session.get(models.User,admin.id)
    if not current_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_user = session.get(models.User,user_id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found!")
    
    return current_user

#===============================
        #RESTRICT A USER
#===============================
'''@router.post("/users/{user_id}")
def restrict_user(user_id: int, user = Depends(admin_access),
                  session: Session = Depends(get_session)):

    current_user = session.get(models.User,user.id)
    if not current_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_user = session.get(models.User,user_id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found!")
    
    return'''

#===============================
        #DELETE A USER
#===============================
@router.delete("/users/{user_id}")
def delete_user(user_id: int, admin = Depends(admin_access),session: Session = Depends(get_session)):

    current_user = session.get(models.User,admin.id)
    if not current_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_user = session.get(models.User,user_id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found!")
    
    session.delete(db_user)
    session.commit()
    return {"message":"User deleted successfully!"}

#======================================================================
                            #ORDERS
#======================================================================
#===============================
        #GET ALL ORDERS
#==============================
@router.get("/orders",response_model=list[schemas.Base_Order_Out])
def get_all_orders(admin = Depends(admin_access),
               session: Session = Depends(get_session)):
    
    current_user = session.get(models.User,admin.id)
    if not current_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_orders = session.query(models.Order).all()
    if not db_orders:
        raise HTTPException(status_code=404,detail="There is no order yet!")
    
    return db_orders

#======================================================================
                            #PRODUCTS
#======================================================================
#===============================
        #GET ALL PRODUCTS
#===============================
@router.get("/products",response_model=list[schemas.Base_Product_Out])
def get_all_products(limit: int = 10, offset: int = 0,
                    admin = Depends(admin_access),
                    session: Session = Depends(get_session)):

    current_user = session.get(models.User,admin.id)
    if not current_user:
        raise HTTPException(status_code=401,detail="User not logged in!")
    
    db_products = session.query(models.Product).all()
    if not db_products:
        raise HTTPException(status_code=404,detail="There is no products yet")
    
    return db_products

#===============================
        #GET PRODUCT BY ID
#===============================
@router.get("/products/{product_id}",response_model=schemas.Base_Product_Out)
def get_product_by_id(product_id: int, admin = Depends(admin_access),
                      session: Session = Depends(get_session)):
    
    current_user = session.get(models.User,admin.id)
    if not current_user:
        raise HTTPException(status_code=401,detail="User not logged in!")
    
    db_product = session.get(models.Product,product_id)
    if not db_product:
        raise HTTPException(status_code=404,detail="Product not found!")
    
    return db_product

#===============================
        #ADD A PRODUCT
#===============================
@router.post("/products",response_model=schemas.Base_Product_Out)
def add_prodcuct(product_input: schemas.Product_Create,
                 current_user = Depends(admin_access),
                 session: Session = Depends(get_session)):
    
    db_user = session.get(models.User,current_user.id)
    if not db_user:
        raise HTTPException(status_code=401,detail="User not logged in!")
    
    new_product = models.Product(
        name = product_input.name,
        stock = product_input.stock,
        price = product_input.price,
    )
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

#===============================
        #UPDATE A PRODUCT
#===============================
@router.put("/products/{product_id}",response_model=schemas.Base_Product_Out)
def update_product(product_id: int, product_updates: schemas.Product_Update,
                    current_user = Depends(admin_access),
                    session: Session = Depends(get_session)):
    
    db_user = session.get(models.User,current_user.id)
    if not db_user:
        raise HTTPException(status_code=401,detail="User not logged in!")
    
    db_product = session.get(models.Product,product_id)
    if not db_product:
        raise HTTPException(status_code=404,detail="Product not found!")
    
    db_product.name = product_updates.name
    db_product.price = product_updates.price
    db_product.stock = product_updates.stock

    session.commit()
    session.refresh(db_product)
    return db_product

#===============================
        #DELETE A PRODUCT
#===============================
@router.delete("/products/{product_id}")
def delete_product(product_id: int,
                    current_user = Depends(admin_access),
                    session: Session = Depends(get_session)):
    
    db_user = session.get(models.User,current_user.id)
    if not db_user:
        raise HTTPException(status_code=401,detail="User not logged in!")
    
    db_product = session.get(models.Product,product_id)
    if not db_product:
        raise HTTPException(status_code=404,detail="Product not found!")
    
    session.delete(db_product)
    session.commit()
    return{"message":"Product deleted successfully!"}