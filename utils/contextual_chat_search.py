from qdrant_client import QdrantClient
from utils.generate_embeddings import get_embedding, ollama_embed
from utils.chat_completions import chat_completion
from utils.config import QDRANT_COLLECTION, QDRANT_ENDPOINT, OLLAMA_QDRANT_COLLECTION
from langchain_openai import ChatOpenAI
from utils.config import MODEL, ENDPOINT
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def contextual_chat_search_with_history(user_query, chat_history=[], is_ollama=False):
    chat_history.append(HumanMessage(content=user_query))

    if is_ollama:
        qdrant_client = QdrantClient(url=OLLAMA_QDRANT_COLLECTION)
    else:
        qdrant_client = QdrantClient(url=QDRANT_ENDPOINT)

    if is_ollama:
        query_vector = ollama_embed(user_query)
    else:
        response = get_embedding(user_query)
        query_vector = response.embedding,

    result = qdrant_client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=query_vector,
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


def contextual_chat_search(user_query, stream=False, is_ollama=False):
    qdrant_client = QdrantClient(url=QDRANT_ENDPOINT)

    if is_ollama:
        collection_name = OLLAMA_QDRANT_COLLECTION

        query_vector = ollama_embed(user_query)
    else:
        collection_name = QDRANT_COLLECTION

        response = get_embedding(user_query)
        query_vector = response.embedding,

    result = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=3,
        search_params={
            # "hnsw_ef": 256
            "hnsw_ef": 512,
            # "quantization": {
            #     "rescore": True
            # }
        },
    )

    # debug
    # for doc in result:
    #     print("\n")
    #     print(doc.score)
    #     print(doc.payload['content'])
    #     print("\n")
    # exit()

    # all content above score of 0.6, and merge content
    context = [doc.payload['content'] for doc in result if doc.score > 0.4]

    # debug
    # context = ""
    # print(context)
    # exit()

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
