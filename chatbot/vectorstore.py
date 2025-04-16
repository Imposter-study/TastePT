from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from abc import ABC, abstractmethod
from django.conf import settings
from threading import Lock
import os


# 벡터 DB 인터페이스 추상화
class VectorStoreBase(ABC):
    @abstractmethod
    def add_file(self, file_path):
        pass

    @abstractmethod
    def as_retriever(self, **kwargs):
        pass

 

class ChromaVectorStore(VectorStoreBase):
    _instance = None
    _lock = Lock()
    file_path = os.path.join(settings.BASE_DIR, "vectors_data")

    def __new__(cls, persist_directory=file_path):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, persist_directory=file_path):
        if hasattr(self, "_initialized") and self._initialized:
            return
        
        self.db = Chroma(
            persist_directory=persist_directory,
            embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002"),
        )
        self._initialized = True

    def add_file(self, file_path):
        loader = CSVLoader(file_path=file_path, encoding="utf-8")
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=700, chunk_overlap=150
        )
        splits = text_splitter.split_documents(data)
        texts = [doc.page_content for doc in splits]
        metadatas = [doc.metadata for doc in splits]
        self.db.add_texts(texts, metadatas=metadatas)

    # 검색 기본값으로 MMR 방식 적용
    def as_retriever(self, **kwargs):
        kwargs.setdefault("search_type", "mmr")
        kwargs.setdefault("search_kwargs", {"k": 3, "fetch_k": 5})
        return self.db.as_retriever(**kwargs)