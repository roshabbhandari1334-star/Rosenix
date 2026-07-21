from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams, Distance
from backend.config.settings import settings

class VectorDatabase:
    def __init__(self):
        self.client = AsyncQdrantClient(url=settings.QDRANT_URL)

    async def init_collection(self, collection_name: str, vector_size: int = 1536):
        collections = await self.client.get_collections()
        existing_names = [c.name for c in collections.collections]
        
        if collection_name not in existing_names:
            await self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )

vector_db = VectorDatabase()