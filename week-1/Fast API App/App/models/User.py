from App.database import Base
from sqlalchemy import Column,Integer,String,Boolean

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    Username=Column(String)
    Hashed_password=Column(String)
    is_admin=Column(Boolean,default=False)
    is_active=Column(Boolean,default=True)






