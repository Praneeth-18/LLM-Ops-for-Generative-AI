import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import logging
import yaml
from datetime import datetime
from typing import Dict, List
import json

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Analyzer</title>
    <script src="https://unpkg.com/react@17/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@17/umd/react-dom.production.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="/static/js/app.js" defer></script>
</head>
<body>
    <div id="root"></div>
</body>
</html>
"""

class DocumentAnalyzer:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.load_config(config_path)
        self.setup_llm()
        self.initialize_vector_store()
        
    def load_config(self, config_path: str):
        try:
            with open(config_path, 'r') as file:
                self.config = yaml.safe_load(file)
            os.environ["OPENAI_API_KEY"] = self.config['openai_api_key']
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            raise
        
    def setup_llm(self):
        try:
            self.llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=0.3
            )
            self.embeddings = OpenAIEmbeddings()
        except Exception as e:
            logger.error(f"Error setting up LLM: {str(e)}")
            raise
        
    def initialize_vector_store(self):
        try:
            if os.path.exists("vectorstore"):
                self.vector_store = FAISS.load_local("vectorstore", self.embeddings)
            else:
                self.vector_store = FAISS.from_texts(["initialization"], self.embeddings)
        except Exception as e:
            logger.error(f"Error initializing vector store: {str(e)}")
            raise
            
    def process_document(self, content: str, metadata: Dict) -> Dict:
        try:
            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = text_splitter.split_text(content)
            
            # Add to vector store with metadata
            self.vector_store.add_texts(
                chunks,
                metadatas=[metadata for _ in chunks]
            )
            
            # Save vector store
            self.vector_store.save_local("vectorstore")
            
            # Get initial analysis
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever()
            )
            
            analysis = qa_chain.run("Provide a brief summary of the main topics in this document.")
            
            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata,
                "analysis": analysis
            }
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise

analyzer = DocumentAnalyzer()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_TEMPLATE

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    logger.debug(f"Received file: {file.filename}")
    
    try:
        # Check file size and type
        content = await file.read()
        if len(content) > 1024 * 1024 * 10:  # 10MB limit
            return JSONResponse(
                status_code=400,
                content={"error": "File too large. Maximum size is 10MB"}
            )
            
        try:
            content = content.decode("utf-8")
        except UnicodeDecodeError:
            return JSONResponse(
                status_code=400,
                content={"error": "File must be a valid text document"}
            )
        
        metadata = {
            "filename": file.filename,
            "timestamp": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        try:
            result = analyzer.process_document(content, metadata)
            return JSONResponse(content=result)
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"error": f"Error processing document: {str(e)}"}
            )
            
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Upload error: {str(e)}"}
        )

@app.get("/query")
async def query_documents(question: str):
    try:
        qa_chain = RetrievalQA.from_chain_type(
            llm=analyzer.llm,
            chain_type="stuff",
            retriever=analyzer.vector_store.as_retriever()
        )
        
        answer = qa_chain.run(question)
        return JSONResponse(content={"question": question, "answer": answer})
    except Exception as e:
        logger.error(f"Error querying documents: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Error querying documents: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)