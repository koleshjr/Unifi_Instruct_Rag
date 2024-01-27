import os 
from langchain_community.document_loaders import PyPDFLoader

class DocumentLoader:
    def __init__(self):
        pass

    def load_and_get_text(self, folder_path: str):
        docs = []

        for file in os.listdir(folder_path):
            try:
                if file.endswith(".pdf"):
                    file_path = os.path.join(folder_path, file)
                    loader = PyPDFLoader(file_path)
                    pages = loader.load_and_split()
                    docs.extend(pages)
            except Exception as e:
                print(f"Error loading file {file} with error {e}") 

        return docs

                

