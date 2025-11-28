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


#Load documents
documents = [
    Document(page_content="Meeting notes: Discuss project X deliverables."),
    Document(page_content="Reminder: Submit report by Friday."),
    Document(page_content="Upcoming event: Tech conference next wednesday."),
]

#Create Embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

#split text for better retrieval
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
docs= text_splitter.split_documents(documents)

#Store embeddings in ChromaDB
vector_db = Chroma.from_documents(docs, embedding = embeddings, persist_directory=CHROMA_DB_PATH)
print("Documents successfully indexed")

