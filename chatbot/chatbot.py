# LangChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Langfuse(챗봇 트레이싱 및 운영툴)
from langfuse import Langfuse
from langfuse.callback import CallbackHandler

from rank_bm25 import BM25Okapi

from django.conf import settings
from .vectorstore import ChromaVectorStore

# Langfuse config 설정을 settings에서 가져오기
langfuse = Langfuse(**settings.LANGFUSE_CONFIG)
langfuse_handler = CallbackHandler(**settings.LANGFUSE_CONFIG)


class Chatbot_Run:
    def __init__(self):
        print("Initializing RAGManager...")

        # LLM 설정
        self.llm = ChatOpenAI(model_name="gpt-4.1-nano", temperature=0.9)

        # 프롬프트 불러오기
        langfuse_prompt = langfuse.get_prompt("TastePT")

        self.prompt = ChatPromptTemplate.from_template(
            langfuse_prompt.get_langchain_prompt(),
            metadata={"langfuse_prompt": langfuse_prompt},
        )

        self.db = ChromaVectorStore()
        self.retriever = self.db.as_retriever()

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

        # 문서 내용 추출 (예시: 'content' 필드에 본문이 있다고 가정)
        documents = [doc.page_content for doc in mmr_recipes]

        # 토크나이즈 (띄어쓰기 기준)
        tokenized_corpus = [doc.split() for doc in documents]
        bm25 = BM25Okapi(tokenized_corpus)

        tokenized_query = query.split()
        bm25_scores = bm25.get_scores(tokenized_query)

        # 점수와 문서 묶어서 내림차순 정렬
        ranked_docs = sorted(zip(bm25_scores, mmr_recipes), key=lambda x: x[0], reverse=True)

        # 리랭킹된 문서 리스트
        reranked_recipes = [doc for score, doc in ranked_docs]
        input_data = {
            "recipes": reranked_recipes,
            "question": query,
            "user_data": user_data,
            "chat_history": chat_history,
        }
        # str으로 변환
        input_data_str = str(input_data)

        return await self.rag_chain.ainvoke(
            input_data_str, config={"callbacks": [langfuse_handler]}
        )
