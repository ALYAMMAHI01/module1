pip install langchain langchain-community langchain-openai
pip install chromadb python-docx

from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
import os


def llm_answer(question: str, context: str) -> str:
    """
    Module 5 Q7:
    Function that sends a question to an LLM and returns an answer
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    prompt = f"""
You must answer the question using ONLY the context below.
If the answer is not in the context, say "Not found in the document".

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)
    return response.content



loader = Docx2txtLoader("data/my_document.docx")
documents = loader.load()


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = splitter.split_documents(documents)


embeddings = OpenAIEmbeddings()

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
vectorstore.persist()


retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


question = input("Ask a question from the document: ")


docs = retriever.get_relevant_documents(question)


context = "\n\n".join([doc.page_content for doc in docs])


answer = llm_answer(question, context)


print("\n Top 3 Retrieved Chunks:\n")
for i, doc in enumerate(docs, 1):
    print(f"Chunk {i}:\n{doc.page_content}\n{'-'*40}")

print("\nFinal Answer:\n")
print(answer)
