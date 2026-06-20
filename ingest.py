import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

def ingest_documents():
    print("Loading PDFs from data/ folder...")
    loader = PyPDFDirectoryLoader("data/")
    documents = loader.load()
    print(f"Loaded {len(documents)} pages")

    print("Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    print("Embedding and uploading to Pinecone...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=os.getenv("PINECONE_INDEX_NAME")
    )
    print("Done! Documents ingested into Pinecone successfully.")

if __name__ == "__main__":
    ingest_documents()
