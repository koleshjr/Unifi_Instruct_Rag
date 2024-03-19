import os 
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings
from langchain_mistralai import MistralAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from dotenv import load_dotenv

class Embeddings:
    def __init__(self, embedding_provider: str):
        load_dotenv()
        self.embedding_provider = embedding_provider

    def get_embedding_function(self):
        if self.embedding_provider == 'openai':
            return OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'), model = "text-embedding-3-large")
        elif self.embedding_provider == 'google':
            return GoogleGenerativeAIEmbeddings(model = 'models/embedding-001', google_api_key=os.getenv('GOOGLE_API_KEY'))
        elif self.embedding_provider == 'mistral':
            return MistralAIEmbeddings(mistral_api_key=os.getenv('MISTRAL_API_KEY'))
        elif self.embedding_provider == 'huggingface':
            model_name = "BAAI/bge-large-en-v1.5"
        elif self.embedding_provider == 'huggingface':
            model_name = "BAAI/bge-small-en"
            model_kwargs = {"device": "cpu"}
            encode_kwargs = {"normalize_embeddings": True}
            hf = HuggingFaceBgeEmbeddings(
                model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
            )
            return hf
        elif self.embedding_provider == 'azure':
            return AzureOpenAIEmbeddings(azure_deployment = "gpt-35-turbo", openai_api_version = "2023-05-15")
          
        else:
            raise Exception("Invalid embedding provider we currently support only openai, google, mistral and huggingface")
        