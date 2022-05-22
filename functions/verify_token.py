def verify_token(email_id,token,mongoDbHandler):
    print("####$$$$$$$$$$$$$$$$$$$$#############")
    result= mongoDbHandler.find(collection_name="session",query={"_id":email_id})
    # print(result)
    for doc in result:
        stored_token=doc["token_id"]
    if token==stored_token :
        return True
    else:
        return False

