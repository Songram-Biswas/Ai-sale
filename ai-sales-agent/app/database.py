# from pymongo import MongoClient
# import logging
# from app.config import Config

# logger = logging.getLogger(__name__)

# class Database:
#     def __init__(self):
#         try:
#             self.client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
#             self.db = self.client.sales_db
#             self.collection = self.db.research_reports
#             self.client.server_info()
#             logger.info("Connected to MongoDB successfully.")
#         except Exception as e:
#             logger.warning(f"MongoDB connection failed: {e}. Proceeding without persistence.")
#             self.collection = None

#     def save_report(self, data: dict):
#         if self.collection is not None:
#             return self.collection.insert_one(data)
#         return None
from pymongo import MongoClient
from app.config import Config

class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client.ai_sales_agent
        self.collection = self.db.reports

    def save_report(self, data):
        return self.collection.insert_one(data)