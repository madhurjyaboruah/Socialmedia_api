
from typing import Collection
from unittest import result
import pymongo

class MongoDbHandler:
    def __init__(self,mongoUrl:str,DatabaseName:str):
        self.__mongoUrl = mongoUrl
        self.__databasename = DatabaseName
        self.__mongodatabase=self.connectToMongoDatabase(self.__mongoUrl,self.__databasename)
 
    def connectToMongoDatabase(self,mongoUrl:str,databasename:str):
        client=pymongo.MongoClient(mongoUrl)
        mydb = client[databasename]
        return mydb
    def count_documents(self,collection_name:str,query:dict):
        if collection_name in self.__mongodatabase.list_collection_names():
            result=self.__mongodatabase[collection_name].count_documents(query)
            return result
    def insert_one(self,collection_name,doc:dict):
        if collection_name in self.__mongodatabase.list_collection_names():
            result = self.__mongodatabase[collection_name].insert_one(doc)
            print(result)
            return result
        else:
            print("collection not found")
    def delete_one(self,collection_name:str,query:dict):
        if collection_name in self.__mongodatabase.list_collection_names():
            result = self.__mongodatabase[collection_name].delete_one(query)
            return result
    def find(self,collection_name:str,query:dict):
        if collection_name in self.__mongodatabase.list_collection_names():
            result =self.__mongodatabase[collection_name].find(query)
            # print(result)
            return result
    def update_one(self,collection_name:str,myquery:dict,newvalues:dict):
         if collection_name in self.__mongodatabase.list_collection_names():
             result = self.__mongodatabase[collection_name].update_one(myquery,newvalues)
             return result



        #       # client = pymongo.MongoClient("mongodb://localhost:27017/")
        # # mydb = client["testapi"]
        # # studentCol = mydb["student"]
        # # sessioncol = mydb["session"]
        # self.__mongoDbHandler.count_documents(collection_name="student", query={"_id":user.email_id})
