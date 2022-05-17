# from unittest import result
from unittest import result
from fastapi import FastAPI, Body, Header
import hashlib
import os
import base64
from App.user_detail import UserDetailsHandler
# from pydantic import BaseModel
from models import models
from functions import verify_token
# from mongoengine import connect
import pymongo
# from bson.objectid import ObjectId
import uvicorn



# mongo_connect =  connect(db="testapi", host="localhost", port=27017)
client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["testapi"]
studentCol = mydb["student"]
sessioncol = mydb["session"]

app = FastAPI()

userdetailshandler = UserDetailsHandler()

@app.post('/create_user')
async def create_user(user: models.User):
    result=userdetailshandler.createuser(user,studentCol)
    return result
   

@app.post('/login')
async def login(login_data: models.Login):
    result=userdetailshandler.userlogin(login_data,studentCol,sessioncol)
    return result


@app.post('/user_details')
async def user_details(email_id:str=Header("email_id", convert_underscores=False),token:str=Header("token")):
    result = userdetailshandler.userdetails(email_id,token,studentCol,sessioncol)
    return result

@app.delete('/delete_user')
async def delete_user(email_id:str=Header("email_id", convert_underscores=False),token:str=Header("token")):
    result=userdetailshandler.deleteuser(email_id,token,studentCol,sessioncol)
    return result
    


   
@app.patch('/user_update')
async def user_update(update:models.Update,email_id:str=Header("email_id", convert_underscores=False),token:str=Header("token")):
    result = userdetailshandler.userupdate(email_id,token,update,studentCol,sessioncol)
   
@app.get('/verify/{id}')
async def verify(id, email_id: str= Header('email_id', convert_underscores=False), token: str= Header('token')):
    print(id)
    result = studentCol.find({"_id":id})
    for doc in result:
        return doc

if __name__ == '__main__':
    print(__name__)
    uvicorn.run("main:app", host = "0.0.0.0", port = 8000, reload=True)