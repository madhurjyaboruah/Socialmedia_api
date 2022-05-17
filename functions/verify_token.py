def verify_token(email_id,token,sessioncol):
    result= sessioncol.find({"_id":email_id})
    for doc in result:
        stored_token=doc["token_id"]
    if token==stored_token :
        return True
    else:
        return False

