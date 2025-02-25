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
            ids=[f"{user_id}_user_{len(self.get_memory(user_id)['documents'])}", 
                 f"{user_id}_ai_{len(self.get_memory(user_id)['documents'])}"]  # Unique IDs for user and AI
        )

    def get_memory(self, user_id):
        """ Retrieves stored messages safely """
        try:
            memory_data = self.collection.get(where={"user_id": user_id})
            
            # Ensure no errors if memory is empty
            if not memory_data or "documents" not in memory_data:
                return {"documents": [], "metadatas": [], "ids": []}
            
            # Dynamically adjust requested results to avoid errors
            num_results = min(5, len(memory_data["documents"]))  # Get last 5 or available messages
            return {
                "documents": memory_data["documents"][-num_results:],
                "metadatas": memory_data["metadatas"][-num_results:],
                "ids": memory_data["ids"][-num_results:]
            }
        except Exception as e:
            print(f"Memory Retrieval Error: {e}")
            return {"documents": [], "metadatas": [], "ids": []}  # Return empty structure on failure

memory = Memory()
