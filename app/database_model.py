from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String,Integer,Column,ForeignKey,Float
from sqlalchemy.orm import relationship

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

    product = relationship("PRODUCT",back_populates="customer")

class PRODUCT(Base):
    __tablename__ = "my_product"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    details = Column(String)
    price = Column(Float)
    user_id = Column(Integer,ForeignKey("Customers.id"))

    customer = relationship("CUSTOMER",back_populates="product")