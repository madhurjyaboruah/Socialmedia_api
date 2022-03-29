from pydantic import BaseModel

class User(BaseModel):
    user_name: str
    Age: int
    School : str =None
    email_id: str
    password: str
    

class Login(BaseModel):
    email_id:str
    password: str
   
class Update(BaseModel):
    name :str =None
    Age: int =None
    School: str=None
class Delete(BaseModel):
    password :str
    confirm_password: str