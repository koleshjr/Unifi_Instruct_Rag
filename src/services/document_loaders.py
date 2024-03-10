import os 
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentLoader:
    def __init__(self):
        pass

    def load_and_get_text(self, folder_path: str):
        docs = []
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=64,
            length_function=len,
            is_separator_regex=False,
        )
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
                    elif 'ESG-spreads' in file.lower():
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
                    texts = text_splitter.create_documents(pages_with_str, metadatas=[{"company_name": company_name, "source": file} for _ in pages_with_str])
                    docs.extend(pages)
            except Exception as e:
                print(f"Error loading file {file} with error {e}") 

        return docs

                

