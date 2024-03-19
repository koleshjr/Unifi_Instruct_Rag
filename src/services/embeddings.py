import os
from typing import Optional 
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

    def get_embedding_function(self, api_key: Optional[str] = None):
        if self.embedding_provider == 'openai':
            if api_key:
                return OpenAIEmbeddings(openai_api_key=api_key, model = "text-embedding-3-large")
            else:
                return OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'), model = "text-embedding-3-large")
        elif self.embedding_provider == 'google':
            if api_key:
                return GoogleGenerativeAIEmbeddings(model = 'models/embedding-001', google_api_key=api_key)
            else:
                return GoogleGenerativeAIEmbeddings(model = 'models/embedding-001', google_api_key=os.getenv('GOOGLE_API_KEY'))

        elif self.embedding_provider == 'mistral':
            if api_key:
                return MistralAIEmbeddings(mistral_api_key=api_key)
            else:
                return MistralAIEmbeddings(mistral_api_key=os.getenv('MISTRAL_API_KEY'))
                

        elif self.embedding_provider == 'huggingface':
            model_name = "BAAI/bge-small-en"
            model_kwargs = {"device": "cpu"}
            encode_kwargs = {"normalize_embeddings": True}
            hf = HuggingFaceBgeEmbeddings(
                model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
            )
            return hf

        else:
            raise Exception("Invalid embedding provider we currently support only openai, google, mistral and huggingface")
        