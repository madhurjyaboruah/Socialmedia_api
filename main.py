from fastapi import FastAPI, Body, Header
from App.user_detail import UserDetailsHandler
# from pydantic import BaseModel
from models import models
# from bson.objectid import ObjectId
import uvicorn
from utils import logger
from DataHandler.MongoDbHandler import MongoDbHandler

mongohandler = MongoDbHandler("mongodb://localhost:27017/","testapi")
app = FastAPI()
logger= logger.logging_info(logger)
userdetailshandler = UserDetailsHandler(logger,mongohandler)

@app.post('/create_user')
async def create_user(user: models.User):
    result=userdetailshandler.createuser(user)
    return result
   

@app.post('/login')
async def login(login_data: models.Login):
    result=userdetailshandler.userlogin(login_data)
    return result


@app.post('/user_details')
async def user_details(email_id:str=Header("email_id", convert_underscores=False),token:str=Header("token")):
    result = userdetailshandler.userdetails(email_id,token)
    return result

@app.delete('/delete_user')
async def delete_user(email_id:str=Header("email_id", convert_underscores=False),token:str=Header("token")):
    result=userdetailshandler.deleteuser(email_id,token)
    return result
    


   
@app.patch('/user_update')
async def user_update(update:models.Update,email_id:str=Header("email_id", convert_underscores=False),token:str=Header("token")):
    result = userdetailshandler.userupdate(email_id,token,update)
    return result
   
# @app.get('/verify/{id}')
# async def verify(id, email_id: str= Header('email_id', convert_underscores=False), token: str= Header('token')):
#     print(id)
#     result = studentCol.find({"_id":id})
#     for doc in result:
#         return doc

if __name__ == '__main__':
    print(__name__)
    uvicorn.run("main:app", host = "0.0.0.0", port = 8000, reload=True)