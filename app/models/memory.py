import chromadb

class Memory:
    def __init__(self):
        self.db = chromadb.PersistentClient(path="./memory")
        self.collection = self.db.get_or_create_collection("chat_memory")

    def store_message(self, user_id, message, response):
        self.collection.add(
            documents=[message, response], 
            metadatas=[{"user_id": user_id}], 
            ids=[str(user_id)]
        )

    def get_memory(self, user_id):
        return self.collection.get(ids=[str(user_id)])

memory = Memory()
