import chromadb
from chromadb.utils import embedding_functions
from chromadb.api.types import EmbeddingFunction
from backend.database import Meeting
from typing import cast

# Create ChromaDB client
chroma_client = chromadb.PersistentClient(path="Data/chroma_db")

# Embedding function
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create collection with cast (fixes Pylance typing complaints)
collection = chroma_client.get_or_create_collection(
    name="meetings",
    embedding_function=cast(EmbeddingFunction, embedding_fn)
)


def index_meeting(meeting: Meeting):
    """Index a meeting transcript + summary into ChromaDB."""
    text_to_index = f"Transcript: {meeting.transcript}\nSummary: {meeting.summary}"
    collection.add(
        documents=[text_to_index],
        metadatas=[{"id": meeting.id, "filename": meeting.filename}],
        ids=[str(meeting.id)]
    )


def semantic_search(query: str, top_k: int = 3):
    """Search meetings by semantic similarity."""
    results = collection.query(query_texts=[query], n_results=top_k)

    documents = results.get("documents") or []
    metadatas = results.get("metadatas") or []

    output = []
    if documents and metadatas:
        for doc, meta in zip(documents[0], metadatas[0]):
            output.append({
                "filename": str(meta.get("filename", "")),
                "id": str(meta.get("id", "")),
                "match_text": doc
            })
    return output
