import os 
from typing import Optional
from langchain_openai import ChatOpenAI, OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from dotenv import load_dotenv
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from langchain_openai import AzureOpenAI

class Llms:
    def __init__(self, model_provider: str, model_name: Optional[str] = None):
        load_dotenv()
        self.model_provider = model_provider
        self.model_name = model_name

    def get_chat_model(self):
        if self.model_provider == 'openai':
            return ChatOpenAI(model= self.model_name, openai_api_key=os.getenv('OPENAI_API_KEY'))
        elif self.model_provider == 'google':
            return ChatGoogleGenerativeAI(model = self.model_name, google_api_key=os.getenv('GOOGLE_API_KEY'))
        else:
            raise Exception("Invalid model provider we currently support only openai and google models")
        
    def get_llm(self):
        if self.model_provider == 'openai':
            return OpenAI(model= self.model_name, openai_api_key=os.getenv('OPENAI_API_KEY'))
        elif self.model_provider == 'google':
            return GoogleGenerativeAI(model = self.model_name, google_api_key=os.getenv('GOOGLE_API_KEY'),safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
            })
        elif self.model_provider == 'azure':
            return AzureOpenAI(deployment_name = self.model_name)
        
        else:
            raise Exception("Invalid model provider we currently support only openai and google models")