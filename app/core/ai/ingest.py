from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
CHROMA_PATH = Path(os.environ["CHROMA_PATH"])
DOCS_PATH = Path(os.environ["DOCS_PATH"])

def ingest():
    documents = []
    for file in os.listdir(DOCS_PATH):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DOCS_PATH, file))
            documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    chunks = splitter.split_documents(documents)
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    Chroma.from_documents(
        chunks,
        embedding = embeddings,
        persist_directory=str(CHROMA_PATH)
    )
    print(f"Ingested {len(chunks)} chunks into Chroma.")

if __name__ == "__main__":
    ingest()