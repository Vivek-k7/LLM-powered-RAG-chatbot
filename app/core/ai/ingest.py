from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from collections import defaultdict
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
CHROMA_PATH = Path(os.environ["CHROMA_PATH"])
DOCS_PATH = Path(os.environ["DOCS_PATH"])
from app.core.ai.prompt import get_chunk_context_prompt


def get_page_context(source, page, pages_by_source):
    texts = []

    for p in (page - 1, page, page + 1):
        if p in pages_by_source[source]:
            texts.append(pages_by_source[source][p])

    return "\n".join(texts)


# To convert docs into embeddings
def ingest():
    documents = []
    for file in os.listdir(DOCS_PATH):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DOCS_PATH, file))
            documents.extend(loader.load())

    llm = ChatOllama(
        model="llama3",
        temperature=0
    )

    pages_by_source = defaultdict(dict)

    for doc in documents:
        source = doc.metadata["source"]
        page = doc.metadata.get("page", 0)
        pages_by_source[source][page] = doc.page_content
    
    # Splits doc into chunks of size = 1000 characters
    # 200 characters overlap(sort of sliding window)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 100
    )
    # apply the split to the docs to get the chunks
    chunks = splitter.split_documents(documents)

    context_prompt = get_chunk_context_prompt()

    # Contextual Chunking: done to add context to chunks which may not be captured fully with normal chunking mechanisms
    for chunk in chunks:
        source = chunk.metadata["source"]
        page = chunk.metadata.get("page", 0)

        page_context = get_page_context(
            source,
            page,
            pages_by_source
        )
        context = context_prompt.invoke({
            "WHOLE_DOCUMENT": page_context,              # +- 1 page around the chunk
            "CHUNK_CONTENT": chunk.page_content
        })

        contextual_summary = llm.invoke(context).content

        chunk.page_content = (
            f"Context:\n{contextual_summary}\n\n"
            f"Chunk:\n{chunk.page_content}"
        )


    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"             # embedding model initialisation
    )

    # convert chunks into embeddings and persist them in a Chroma vector store
    Chroma.from_documents(
        chunks,
        embedding = embeddings,
        persist_directory=str(CHROMA_PATH)
    )
    print(f"Ingested {len(chunks)} chunks into Chroma.")

if __name__ == "__main__":
    ingest()