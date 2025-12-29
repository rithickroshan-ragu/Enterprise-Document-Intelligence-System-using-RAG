import os
import shutil

from pypdf import PdfReader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document


class Vectorstore:
    def __init__(self, db_path):
        self.db_path = db_path
        self.chunk_size = 100

    def _instantiate_embedding_model(self):
        embedding_model= OpenAIEmbeddings(
            model=os.getenv("OPENAI_EMBEDDING_MODEL"),
            base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY")
        )

        return embedding_model

    def initialize_vectorstore(self):
        embedding_model = self._instantiate_embedding_model()
        self.vectorstore = Chroma(
            collection_name="document_collection",
            embedding_function=embedding_model,
            persist_directory=self.db_path
        )

    def add_documents(self, path):
        documents = self._read_and_chunk_pdf(path)
        self.vectorstore.add_documents(documents)
    
    def similarity_search(self, query):
        return self.vectorstore.similarity_search(query)
    
    def reset_collection(self):
        """Safely clear the persistent Chroma data."""
        # # remove the persisted DB files
        # if os.path.exists(self.db_path):
        #     try:
        #         shutil.rmtree(self.db_path)
        #     except Exception:
        #         # if remove fails, continue and attempt to recreate the directory
        #         pass

        # recreate the directory and reinitialize the vectorstore
        # os.makedirs(self.db_path, exist_ok=True)
        # self.initialize_vectorstore()
        self.vectorstore.reset_collection()

    def _read_and_chunk_pdf(self, path):
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        documents = [] 
        for i in range(0, len(text), self.chunk_size):
            documents.append(Document(text[i:i + self.chunk_size]))
        
        return documents
    
        


    
