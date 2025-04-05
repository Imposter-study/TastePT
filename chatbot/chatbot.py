# LangChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Langfuse(챗봇 트레이싱 및 운영툴)
from langfuse import Langfuse
from langfuse.callback import CallbackHandler

from threading import Lock
import os


from django.conf import settings
from .models import Recipe

# Langfuse config 설정을 settings에서 가져오기
langfuse = Langfuse(**settings.LANGFUSE_CONFIG)
langfuse_handler = CallbackHandler(**settings.LANGFUSE_CONFIG)


# 레시피 임베딩 및 백터DB저장
class VectorStoreManager:
    _instance = None
    _lock = Lock()

    # 임베딩 후 벡터 DB저장 위치
    file_path = os.path.join(settings.BASE_DIR, "vectors_data")

    def __new__(cls, persist_directory=file_path):

        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize_vectorstore(persist_directory)
        return cls._instance

    # 벡터 DB 초기화 영구 저장 설정
    def _initialize_vectorstore(self, persist_directory):

        print("Initializing VectorStoreManager with ChromaDB...")

        self.db = Chroma(
            persist_directory=persist_directory,
            embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002"),
            collection_metadata={
                "hnsw:space": "cosine",
            },
        )
        self.retriever = self.db.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 3,
                "fetch_k": 10,
            },
        )

        print(" Vector Store is ready!")

    def get_retriever(self):
        with self._lock:
            return self.retriever

    def add_file(self):
        csv_files = Recipe.objects.filter(is_embedded=False)

        #  예외 처리: 업로드된 CSV가 없을 경우
        if not csv_files.exists():
            print(" No unembedded CSV files found.")
            return

        # 파일 불러와 벡터 DB에 추가
        for file_obj in csv_files:
            file_path = file_obj.csv_file.path
            print(f"Loading {file_path}...")

            #  CSV 로드 및 문서 변환
            loader = CSVLoader(file_path=file_path, encoding="utf-8")
            data = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=700, chunk_overlap=150
            )
            splits = text_splitter.split_documents(data)

            # 벡터 DB에 올바르게 추가 (텍스트 & 메타데이터 분리)
            texts = [doc.page_content for doc in splits]
            metadatas = [doc.metadata for doc in splits]
            self.db.add_texts(texts, metadatas=metadatas)

            print(f"{file_path} loaded successfully!")

            # CSV 파일을 벡터 DB에 추가했으므로, `is_embedded=True`로 업데이트
            file_obj.is_embedded = True
            file_obj.save()


class Chatbot_Run:
    def __init__(self):
        print("Initializing RAGManager...")

        # LLM 설정
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.9)

        # 프롬프트 불러오기
        langfuse_prompt = langfuse.get_prompt("TastePT")

        self.prompt = ChatPromptTemplate.from_template(
            langfuse_prompt.get_langchain_prompt(),
            metadata={"langfuse_prompt": langfuse_prompt},
        )

        self.db = VectorStoreManager()
        self.retriever = self.db.get_retriever()

        # RAG Chain 생성
        self.rag_chain = (
            {
                "recipes": self.retriever,
                "question": RunnablePassthrough(),
                "user_data": RunnablePassthrough(),
                "chat_history": RunnablePassthrough(),
            }
            | self.prompt
            | self.llm
        )


    async def ask(self, query: str, user_data, chat_history):
        # MMR로 문서 검색 후 BM25 기반 리랭킹
        mmr_recipes = await self.retriever.ainvoke(query)
        input_data = {
            "recipes": mmr_recipes,
            "question": query,
            "user_data": user_data,
            "chat_history": chat_history,
        }
        # str으로 변환
        input_data_str = str(input_data)

        return await self.rag_chain.ainvoke(
            input_data_str, config={"callbacks": [langfuse_handler]}
        )
