import os 
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma, Milvus

class VectorStore:
    def __init__(self, vector_store: str, index_name: str):
        load_dotenv()
        self.vector_store = vector_store
        self.index_name = "src/indexes/" + index_name 

    def store_embeddings(self, embedding_function: str, docs: list):
        if self.vector_store == 'chroma':
            vector_index = Chroma.from_documents(documents = docs, embedding = embedding_function,  persist_directory = self.index_name)
            return vector_index.persist()
        elif self.vector_store == 'milvus':
            vector_index = Milvus.from_documents(docs, embedding_function, connection_args = {"host": os.getenv('MILVUS_HOST'), "port": os.getenv('MILVUS_PORT'), "collection_name": self.index_name})
            return vector_index.persist()
            
        else:
            raise Exception("Invalid vector store we currently support only chroma and milvus")
