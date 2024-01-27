import os 
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

class Embeddings:
    def __init__(self, embedding_provider: str):
        load_dotenv()
        self.embedding_provider = embedding_provider

    def get_embedding_function(self):
        if self.embedding_provider == 'openai':
            return OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
        elif self.embedding_provider == 'google':
            return GoogleGenerativeAIEmbeddings(model = 'models/embedding-001', google_api_key=os.getenv('GOOGLE_API_KEY'))
        
        else:
            raise Exception("Invalid embedding provider we currently support only openai and google embeddings")
        