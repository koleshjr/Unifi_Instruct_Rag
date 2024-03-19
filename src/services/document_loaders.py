import os 
import nest_asyncio
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
from llama_parse import LlamaParse 
from llama_index.core import SimpleDirectoryReader


class DocumentLoader:
    def __init__(self):
        load_dotenv()
        nest_asyncio.apply()

    def load_and_get_text(self, folder_path: str):
        docs = []
        for file in os.listdir(folder_path):
            try:
                if file.endswith(".pdf"):
                    file_path = os.path.join(folder_path, file)
                    if 'distel' in file.lower():
                        company_name = 'distel'
                    elif 'picknpay' in file.lower():
                        company_name = 'picknpay'
                    elif 'oceana' in file.lower():
                        company_name = 'oceana1&2'
                    elif 'sasol' in file.lower():
                        company_name = 'sasol'
                    elif 'ESG-spreads' in file:
                        company_name = 'impala'
                    elif 'clicks' in file.lower():
                        company_name = 'clicks'
                    elif 'absa' in file.lower():
                        company_name = 'absa'
                    elif 'ssw' in file.lower():
                        company_name = 'ssw'
                    else:
                        company_name = file

                    loader = PyPDFLoader(file_path=file_path)
                    pages = loader.load_and_split()
                    pages_with_str = [doc.page_content for doc in pages]
                    for page in pages_with_str:
                        doc = Document(
                                page_content=page,
                                metadata={
                                    "source": file,
                                    "company_name": company_name,
                                }
                            )
                        docs.append(doc)
 
            except Exception as e:
                print(f"Error loading file {file} with error {e}") 
        return docs
    
    def load_and_get_text_llama_parse(self, folder_path):
        docs = []
        for file in os.listdir(folder_path):
            try:
                if file.endswith(".pdf"):
                    file_path = os.path.join(folder_path, file)
                    if 'distel' in file.lower():
                        company_name = 'distel'
                    elif 'picknpay' in file.lower():
                        company_name = 'picknpay'
                    elif 'oceana' in file.lower():
                        company_name = 'oceana1&2'
                    elif 'sasol' in file.lower():
                        company_name = 'sasol'
                    elif 'ESG-spreads' in file:
                        company_name = 'impala'
                    elif 'clicks' in file.lower():
                        company_name = 'clicks'
                    elif 'absa' in file.lower():
                        company_name = 'absa'
                    elif 'ssw' in file.lower():
                        company_name = 'ssw'
                    else:
                        company_name = file
                    
                    parser = LlamaParse(
                        result_type = "markdown",
                        num_workers = 1,
                        verbose = True
                    )
                    file_extractor = {".pdf": parser}
                    documents = SimpleDirectoryReader(input_files = [file_path], file_extractor = file_extractor).load_data()
                    pages_with_str = documents[0].text.split("\n---")
                    for page in pages_with_str:
                        doc = Document(
                                page_content=page,
                                metadata={
                                    "source": file,
                                    "company_name": company_name,
                                }
                            )
                        docs.append(doc)
 
            except Exception as e:
                print(f"Error loading file {file} with error {e}") 

        return docs
