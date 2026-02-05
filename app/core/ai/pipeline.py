from pathlib import Path
import os
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from dotenv import load_dotenv
load_dotenv()

from .prompt import get_prompt
from .vectorstore import get_retriever

llm = ChatOllama(
    model="llama3",
    temperature=0
)

load_dotenv()
CHROMA_PATH = Path(os.environ["CHROMA_PATH"])
DOCS_PATH = Path(os.environ["DOCS_PATH"])


def retrieval_pipeline(payload):
    query = payload["query"]
    retriever = get_retriever()
    context = retriever.invoke(query)
    prompt = get_prompt()

    chain = (
        {
            "context": lambda _ : context,
            "query": lambda _ : RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke(query)

    return {
        'answer': answer,
        'sources': [],
        "grounded": bool(answer)    
    }
