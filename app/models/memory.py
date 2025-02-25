import chromadb

class Memory:
    def __init__(self):
        self.db = chromadb.PersistentClient(path="./memory")
        self.collection = self.db.get_or_create_collection("chat_memory")

    def store_message(self, user_id, message, response):
        """ Stores user and AI messages while ensuring list lengths match """
        self.collection.add(
            documents=[message, response], 
            metadatas=[{"user_id": user_id}, {"user_id": user_id}],  # Matching length
            ids=[f"{user_id}_user", f"{user_id}_ai"]  # Unique IDs for user and AI
        )

    def get_memory(self, user_id):
        """ Retrieves stored messages for a given user """
        try:
            return self.collection.get(where={"user_id": user_id})  # Fetch by metadata
        except Exception:
            return {"documents": [], "metadatas": [], "ids": []}  # Return empty if not found

memory = Memory()
