from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uvicorn
from utils.config import API_PORT
from utils.chunk_webpage import chunk_webpage
from utils.qdrant_embed import qdrant_embed_docs
from utils.contextual_chat_search import contextual_chat_search_with_history
from utils.error import pretty_print_error

app = FastAPI()

chat_history = []

current_conversation_id = None

class WebpageRequest(BaseModel):
    url: str

class ChatRequest(BaseModel):
    user_query: str
    conversation_id: str

@app.get("/")
def read_root():
    return {"message": "RAG n roll!"}

@app.post("/embed/webpage")
async def embed_webpage(request: WebpageRequest):
    url = request.url

    docs = chunk_webpage(url)

    qdrant_embed_docs(docs, {
        "url": url.strip()
    })
    
    return docs

@app.post("/chat")
async def chat(request: ChatRequest):
    user_query = request.user_query
    conversation_id = request.conversation_id

    # proof of concept only, should be replaced with proper storage
    global chat_history
    global current_conversation_id
    if conversation_id != current_conversation_id:
        current_conversation_id = conversation_id
        chat_history = []

    try:
        response = contextual_chat_search_with_history(user_query, chat_history)

        for message in response['chat_history']:
            print(message)

        return response['response']

    except Exception as e:
        pretty_print_error(e)

        return {
            "error": str(e),
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=API_PORT)
