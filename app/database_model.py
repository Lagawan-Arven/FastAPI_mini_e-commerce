from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String,Integer,Column,ForeignKey,Float
from sqlalchemy.orm import relationship
from app.database import engine

Base = declarative_base()

class CUSTOMER(Base):
    __tablename__ = "Customers"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    age = Column(Integer)
    sex = Column(String)
    occupation = Column(String)

    username = Column(String)
    password = Column(String)

    order = relationship("ORDER",back_populates="customer")

class ORDER(Base):
    __tablename__ = "Orders"

    id = Column(Integer,primary_key=True,index=True)
    customer_id = Column(Integer,ForeignKey("Customers.id"))
    status = Column(String)

    customer = relationship("CUSTOMER",back_populates="order")
    items = relationship("ORDER_ITEM",back_populates="order",cascade="all,delete")

class ORDER_ITEM(Base):
    __tablename__ = "order_items"

    id = Column(Integer,primary_key=True,index=True)
    order_id = Column(Integer,ForeignKey("orders.id"))  
    product_id = Column(Integer,ForeignKey("products.id"))
    quantity = Column(Integer, default=1)

    order = relationship("ORDER",back_populates="items")
    product = relationship("PRODUCT",back_populates="items")

class PRODUCT(Base):
    __tablename__ = "Products"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    details = Column(String)
    stock = Column(Integer)
    price = Column(Float)

    items = relationship("ORDER_ITEM",back_populates="product") 


Base.metadata.create_all(bind=engine)