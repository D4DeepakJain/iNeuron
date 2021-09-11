import  pymongo
class DBHelper:
    def insert(mydict):
        dbConn = pymongo.MongoClient("mongodb://localhost:27017")    
        db = dbConn.WebScrapperDB
        collection = db.WebScrapper
        collection.insert_one(mydict)
    
    def Search(str):
        dbConn = pymongo.MongoClient("mongodb://localhost:27017")    
        db = dbConn.WebScrapperDB
        collection = db.WebScrapper
        reviewCUrsor = collection.find({"Product":str}) 
        reviews = []
        for doc in reviewCUrsor:
            reviews.append(doc)
        return reviews