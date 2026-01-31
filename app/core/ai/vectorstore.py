from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama

from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

CHROMA_PATH = Path(os.environ["CHROMA_PATH"])

# initializes the embedding model and loads the persisted Chroma vector store
# returns a retriever configured to fetch the top-k relevant chunks
def get_retriever():
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    vectorstore = Chroma(
        persist_directory = str(CHROMA_PATH),
        embedding_function = embeddings
    )
    return vectorstore.as_retriever(search_kwargs = {"k": 4})
