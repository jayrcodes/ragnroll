from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uvicorn
from utils.config import API_PORT
from utils.chunk_webpage import chunk_webpage
from utils.qdrant_embed import qdrant_embed_docs
from utils.contextual_chat_search import contextual_chat_search
from utils.error import pretty_print_error

app = FastAPI()

class WebpageRequest(BaseModel):
    url: str

class ChatRequest(BaseModel):
    user_query: str

@app.get("/")
def read_root():
    return {"message": "RAG n roll!"}

@app.post("/embed/webpage")
async def embed_webpage(request: WebpageRequest):
    url = request.url

    docs = chunk_webpage(url)
    qdrant_embed_docs(docs)
    
    return docs

@app.post("/chat")
async def chat(request: ChatRequest):
    user_query = request.user_query

    try:
        response = contextual_chat_search(user_query, stream=False)
    except Exception as e:
        pretty_print_error(e)

        return {
            "error": str(e),
        }
    
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=API_PORT)
