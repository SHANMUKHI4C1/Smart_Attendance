from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://23wh1a04c0:test123@cluster2.fojnwul.mongodb.net/?appName=Cluster2"
)

db = client["attendance_db"]
