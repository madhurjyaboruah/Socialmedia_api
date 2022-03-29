# from unittest import result
from fastapi import FastAPI, Body, Header
import hashlib
import os
import base64
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



@app.post('/create_user')
async def create_user(user: models.User):
    result = studentCol.count_documents({"_id":user.email_id})
    if result != 0:
        return {"messasge": "Email id already exists"}
    else:
        t_hashed = hashlib.sha3_512(user.password.encode())
        hashed_password = t_hashed.hexdigest()
        # print(hashed_password)
        student_doc = { "_id":user.email_id,
                        "name": user.user_name,
                        "Age": user.Age,
                        "School": user.School,
                        "Password":hashed_password

        }
        studentCol.insert_one(student_doc.copy())
        print(student_doc)
        return student_doc

@app.post('/login')
async def login(login_data: models.Login):
    email_id=login_data.email_id
    password=login_data.password
    result = studentCol.find({"_id":email_id})
    for doc in result:
        stored_password = doc["Password"]
    t_hashed = hashlib.sha3_512(password.encode())       #hashing password
    hashedpassword = t_hashed.hexdigest()
    if hashedpassword == stored_password:
        random_byte = os.urandom(64)
        token = base64.b64encode(random_byte).decode('utf-8') 
        result = sessioncol.count_documents({"_id":login_data.email_id})
        if result != 0:
            myquery = { "_id": email_id }
            newvalues = { "$set": {"token_id":token} }
            sessioncol.update_one(myquery, newvalues)
            return {"token":token}
        else:

            session_details = { "_id":login_data.email_id,
                                "token_id" :token
            }
            sessioncol.insert_one(session_details.copy())
            return {"token":token}

@app.post('/user_details')
async def user_details(email_id:str=Header("email_id", convert_underscores=False),token:str=Header("token")):
   
  #  result= sessioncol.find({"_id":email_id})
   # for doc in result:
    #    stored_token=doc["token_id"]
    #if token==stored_token :
    if verify_token.verify_token(email_id,token,sessioncol):
       result=studentCol.find({"_id":email_id})
    for doc in result:
        output={}
        for k,v in doc.items():
            if k.lower()!='password':
                output[k]=v
        return output

@app.delete('/delete_user')
async def delete_user(email_id:str=Header("email_id", convert_underscores=False),token:str=Header("token")):
    # result= sessioncol.find({"_id":email_id})
    # for doc in result:
    #     stored_token=doc["token_id"]
    if verify_token.verify_token(email_id,token,sessioncol):
         myquery = { "_id": email_id }
         studentCol.delete_one(myquery)
         sessioncol.delete_one(myquery)


   
@app.patch('/user_update')
async def user_update(update:models.Update,email_id:str=Header("email_id", convert_underscores=False),token:str=Header("token")):
    if verify_token.verify_token(email_id,token,sessioncol):
        print("yes")
        myquery = { "_id": email_id }
        newvalues = { "$set": dict(update) }
        print(newvalues)
        studentCol.update_one(myquery, newvalues)
    return await user_details(email_id, token)
        
      

    

@app.get('/verify/{id}')
async def verify(id, email_id: str= Header('email_id', convert_underscores=False), token: str= Header('token')):
    print(id)
    result = studentCol.find({"_id":id})
    for doc in result:
        return doc

if __name__ == '__main__':
    print(__name__)
    uvicorn.run("main:app", host = "0.0.0.0", port = 8000, reload=True)