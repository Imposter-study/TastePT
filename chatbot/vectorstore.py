from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from abc import ABC, abstractmethod
from django.conf import settings
from threading import Lock, Thread
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
        
        # 쓰기 락 초기화
        self._write_lock = Lock()
        self.db = Chroma(
            persist_directory=persist_directory,
            embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002"),
        )
        self._initialized = True

    def add_file(self, file_path):
        # 백그라운드 스레드로 임베딩 수행 (기존 DB 조회에는 영향 없음)
        def _background_ingest():
            loader = CSVLoader(file_path=file_path, encoding="utf-8")
            data = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=700, chunk_overlap=150
            )
            splits = text_splitter.split_documents(data)
            texts = [doc.page_content for doc in splits]
            metadatas = [doc.metadata for doc in splits]
            with self._write_lock:
                self.db.add_texts(texts, metadatas=metadatas)

        Thread(target=_background_ingest, daemon=True).start()

    # 검색 기본값으로 MMR 방식 적용
    def as_retriever(self, **kwargs):
        kwargs.setdefault("search_type", "mmr")
        kwargs.setdefault("search_kwargs", {"k": 10, "fetch_k": 20})
        return self.db.as_retriever(**kwargs)