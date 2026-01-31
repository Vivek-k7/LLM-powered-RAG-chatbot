from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """
You are a helpful and accurate assistant.

Answer questions ONLY using the information provided in the supplied documents.

If the answer cannot be found in the documents, respond with:
"Insufficient information in the provided documents."

Be concise, clear, and factual.
"""


def get_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("system", "Context from documents:\n{context}"),
        ("system", "Conversation history:\n{history}"),
        ("human", "{query}")
    ])
