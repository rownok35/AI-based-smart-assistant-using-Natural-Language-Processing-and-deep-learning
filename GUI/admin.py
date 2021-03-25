import pymongo
from pymongo import MongoClient
# from datetime import datetime


# now = datetime.now()
# # dd/mm/YY H:M:S
# dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# # print("date and time =", dt_string)	
# str1="do you know my master"

cluster= MongoClient("mongodb+srv://chatbot:a4s@cluster0.rqhb3.mongodb.net/query?retryWrites=true&w=majority")
db=cluster["query"]
collection=db["query"]
result=collection.find({})
for i in result:
	print(i)