import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever
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

