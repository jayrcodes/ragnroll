from qdrant_client import QdrantClient
from utils.generate_embeddings import get_embedding
from utils.chat_completions import chat_completion
from utils.config import QDRANT_COLLECTION, QDRANT_ENDPOINT
from langchain_openai import ChatOpenAI
from utils.config import MODEL, ENDPOINT
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def contextual_chat_search_with_history(user_query, chat_history = []):
    chat_history.append(HumanMessage(content=user_query))

    qdrant_client = QdrantClient(url=QDRANT_ENDPOINT)

    embedded_query = get_embedding(user_query)

    result = qdrant_client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=embedded_query.embedding,
        limit=3,
        search_params={"hnsw_ef": 256},
    )

    # all content above score of 0.6, and merge content
    context = [doc.payload['content'] for doc in result if doc.score > 0.6]
    # print(context)

    model = ChatOpenAI(
        model=MODEL,
        base_url=ENDPOINT,
        api_key="lm-studio",
    )

    system_message = f"""
    You are a helpful assistant. Answer all questions to the best of your ability.

    Context:
    {context}

    Task:
    {user_query}
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=system_message
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    chain = prompt | model

    ai_msg = chain.invoke(
        {
            "messages": chat_history
        }
    )

    chat_history.append(ai_msg.content)

    return {
        "response": ai_msg,
        "chat_history": chat_history
    }

def contextual_chat_search(user_query, stream=False):
    qdrant_client = QdrantClient(url=QDRANT_ENDPOINT)

    embedded_query = get_embedding(user_query)

    result = qdrant_client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=embedded_query.embedding,
        limit=3,
        search_params={"hnsw_ef": 256},
    )

    # all content above score of 0.6, and merge content
    context = [doc.payload['content'] for doc in result if doc.score > 0.6]
    # print(context)

    prompt = f"""
    Context:
    {context}

    Task:
    {user_query}
    """

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]

    # chat completion but streaming
    response = chat_completion(messages, stream)

    return response