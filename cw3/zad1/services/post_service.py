from repositories.post_respository import PostRepository
from services.ipost_service import IPostService
from typing import List
from domains.post import PostRecord

class PostService:
    repository: PostRepository

    def __init__(self, repository: PostRepository) -> None:
        self.repository = repository
        self._posts_cache: List[PostRecord] = []

    async def fetch_and_cache_posts(self) -> None:
        self._posts_cache = await self.repository.get_all_post_params()

    def filter_posts(self, search_query: str) -> List[PostRecord]:
        return [
            post for post in self._posts_cache
            if search_query.lower() in post.title.lower() or search_query.lower() in post.body.lower()
        ]

    def get_all_posts_as_json(self) -> List[dict]:
        return [post.__dict__ for post in self._posts_cache]