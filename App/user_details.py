from calendar import c
import hashlib
import imp
import logging
import os
import base64

from DataHandler.MongoDbHandler import MongoDbHandler
from functions import verify_token


class UserDetailsHandler:
    def __init__(self,logger: logging, mongoDbHandler: MongoDbHandler):
        self.__logger = logger
        self.__mongoDbHandler = mongoDbHandler

    def createuser(self,user):
        # result = self.studentCol.count_documents({"_id":user.email_id})
        result = self.__mongoDbHandler.count_documents(collection_name="student", query={"_id":user.email_id})
        if result != 0:
            self.__logger.error('user already exist ...')
            return {"error": "Email id already exists"}

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
            self.__mongoDbHandler.insert_one(collection_name="student", doc= student_doc)
            # print(student_doc)
            self.__logger.info('creating user ......')
            del student_doc['Password']
            return student_doc

    def userlogin(self,login_data,token):
        email_id=login_data.email_id
        password=login_data.password
        result =self.__mongoDbHandler.find(collection_name="student",query={"_id":email_id})
        # result = self.studentCol.find({"_id":email_id})
        for doc in result:
            stored_password = doc["Password"]
            t_hashed = hashlib.sha3_512(password.encode())       #hashing password
            hashedpassword = t_hashed.hexdigest()
            if hashedpassword == stored_password:
                random_byte = os.urandom(64)
                token = base64.b64encode(random_byte).decode('utf-8') 
                result= self.__mongoDbHandler.count_documents(collection_name="session",query={"_id":login_data.email_id})
                # result = self.sessionCol.count_documents({"_id":login_data.email_id})
            if result != 0:
                # myquery = { "_id": email_id }
                # newvalues = { "$set": {"token_id":token} }
                #  self.sessionCol.update_one(myquery, newvalues)
                self.__mongoDbHandler.update_one(collection_name="session",query={ "_id": email_id },newvalues={ "$set": {"token_id":token} })
               
                self.__logger.info('user login successfully...')
                return {"token":token}
            else:
                session_details = { "_id":login_data.email_id,
                                    "token_id" :token
                }
                self.sessionCol.insert_one(session_details.copy())
                self.__mongoDbHandler.insert_one(collection_name="session",session_details = { "_id":login_data.email_id,"token_id" :token})
                self.__logger.info('user login successfully 2...')
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
                self.__logger.info('showing the user details ...')
                return output
            else:
                return {"error":"login Required"}
    





    def  userUpdate(self,email_id,token,update):
        if verify_token.verify_token(email_id,token,self.__mongoDbHandler):
            # print("yes")
            result=self.__mongoDbHandler.update_one(collection_name="student",query={"_id":email_id},newvalues={"$set":dict(update)})
        else:
            return {"message": "session expired"}
        return self.userdetails(email_id, token)
    
    def deleteuser(self,email_id,token):
        if verify_token.verify_token(email_id,token,self.__mongoDbHandler):
            self.__mongoDbHandler.delete_one(collection_name="student",query={"_id":email_id})
            self.__mongoDbHandler.delete_one(collection_name="session",query={"_id":email_id})
        else:
            return {"error":"login Required"}



   