import base64
from cgitb import handler
import hashlib
import os
from typing import Collection

from fastapi import Query
from DataHandler.MongoDbHandler import MongoDbHandler
from functions import verify_token
class UserDetailsHandler:
    def __init__(self,logger,mongodbhandler:MongoDbHandler):
        self.__logger= logger
        self.__mongoDbHandler  = mongodbhandler
        # self.sessioncol = sessioncol
        # self.studentCol = studentCol

    def userlogin(self,login_data):
        email_id=login_data.email_id
        password=login_data.password
        result = self.__mongoDbHandler.find(collection_name="student",query={"_id":email_id})
        for doc in result:
            stored_password = doc["Password"]
            t_hashed = hashlib.sha3_512(password.encode())       #hashing password
            hashedpassword = t_hashed.hexdigest()
            if hashedpassword == stored_password:
                random_byte = os.urandom(64)
                token = base64.b64encode(random_byte).decode('utf-8') 
                print("#################")
                result = self.__mongoDbHandler.count_documents(collection_name="session",query={"_id":login_data.email_id})
            if result != 0:
                self.__mongoDbHandler.update_one(collection_name="session",myquery={ "_id": email_id }, newvalues={ "$set": {"token_id":token} })
                self.__logger.info("login succesfully .....")
                return {"token":token}
            else:
                self.__mongoDbHandler.insert_one(collection_name="session",doc={ "_id":login_data.email_id, "token_id" :token })
                return {"token":token}

    def userdetails(self,email_id,token):
        if email_id and token:
            if verify_token.verify_token(email_id,token,self.__mongoDbHandler):
                result=self.__mongoDbHandler.find(collection_name="student",query={"_id":email_id})
                for doc in result:
                    output={}
                    for k,v in doc.items():
                        if k.lower()!='password':
                            output[k]=v
                return output
    def createuser(self,user):
        result = self.__mongoDbHandler.count_documents(collection_name="student",  query={"_id":user.email_id})
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
            self.__mongoDbHandler.insert_one(collection_name="student",doc=student_doc)
            self.__logger.info('creating user ......')
            del student_doc["Password"]
            print(student_doc)
            return student_doc
    
    def deleteuser(self,email_id,token):
        if verify_token.verify_token(email_id,token,self.__mongoDbHandler):
            self.__mongoDbHandler.delete_one(collection_name="student",query={ "_id": email_id })
            self.__mongoDbHandler.delete_one(collection_name="session",query={ "_id": email_id })

    def userupdate(self,email_id,token,update):
        if verify_token.verify_token(email_id,token,self.__mongoDbHandler):
            self.__mongoDbHandler.update_one(collection_name="student",myquery={ "_id": email_id }, newvalues={ "$set": dict(update) })
        return self.userdetails(email_id,token)


