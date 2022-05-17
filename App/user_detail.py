import base64
import hashlib
import os
from functions import verify_token
class UserDetailsHandler:
    def __init__(self):
        pass
    def userlogin(self,login_data,studentCol,sessioncol):
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
                print("#################")
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

    def userdetails(self,email_id,token,studentCol,sessioncol):
        if email_id and token:
            if verify_token.verify_token(email_id,token,sessioncol):
                result=studentCol.find({"_id":email_id})
                for doc in result:
                    output={}
                    for k,v in doc.items():
                        if k.lower()!='password':
                            output[k]=v
                return output
    def createuser(self,user,studentCol):
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
            del student_doc["Password"]
            # print(student_doc)
            return student_doc
    def deleteuser(self,email_id,token,studentCol,sessioncol):
        if verify_token.verify_token(email_id,token,sessioncol):
            myquery = { "_id": email_id }
            studentCol.delete_one(myquery)
            sessioncol.delete_one(myquery)

    def userupdate(self,email_id,token,update,studentCol,sessioncol):
        if verify_token.verify_token(email_id,token,sessioncol):
            myquery = { "_id": email_id }
            newvalues = { "$set": dict(update) }
            studentCol.update_one(myquery, newvalues)
        return  newvalues


