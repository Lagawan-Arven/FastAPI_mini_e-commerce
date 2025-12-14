from pydantic import BaseModel

class Customer_Personal_Info(BaseModel):
    age: int
    firstname: str
    lastname: str
    sex: str
    occupation: str

class Customer_Create(Customer_Personal_Info):
    username: str
    password: str

class Customer_Out(BaseModel):
    id: int
    username: str
    
    class Config:
        from_attributes = True

class Product_ID_List(BaseModel):
    ids: list[int]

class Order_Create(BaseModel):
    items: list[Item] = []
    status: str = "pending"

class Order_Out(Order_Create):
    id: int

    class Config:
        from_attributes = True  

class Item(BaseModel):
    quantity: int
    order_id: int
    product_id: int
    

class Product_Create(BaseModel):
    name: str
    details: str
    stock: int
    price: float

class Product_Out(Product_Create):
    id: int

    class Config:
        from_attributes = True

    

