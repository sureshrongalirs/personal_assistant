import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
import gdown

#Download .env file from gdrive
file_id = "1sRnqJqJckJXKU28uQxf8bHXIL680qnOb"
url = f"https://drive.google.com/uc?id={file_id}"
output = ".env" #Change the filename as needed

gdown.download(url, output, quiet=False)

#Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "db")

#Ensure API key is set
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not found in .env")

#Load stored vector database
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vector_db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
retriever = vector_db.as_retriever() 

#Use GPT-4 for answer generation
llm = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)

#Create Retrieval augmented generation (RAG) chain
qa_chain = load_qa_chain(llm, chain_type="stuff")

def get_response(query):
    """Get response from the RAG system for a given query."""
    docs = retriever.get_relevant_documents(query)
    response = qa_chain.run(input_documents=docs, question=query)
    return response

