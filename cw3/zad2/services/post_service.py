from datetime import datetime

from domains.comment import PostComment
from repositories.post_respository import PostRepository
from services.ipost_service import IPostService
from typing import List
from domains.post import PostRecord

class PostService:
    repository: PostRepository

    def __init__(self, repository: PostRepository) -> None:
        self.repository = repository
        self._posts_cache: List[PostRecord] = []
        self._comments_cache: List[PostComment] = []

    async def load_data(self):
        posts = await self.repository.get_all_post_params()
        comments = await self.repository.get_all_comment_params()

        for post in posts:
            post.comments = [c for c in comments if c.post_id == post.post_id]

        self._posts_cache = posts
        self._comments_cache = comments

    def filter_posts(self, search_query: str) -> List[PostRecord]:
        return [
            post for post in self._posts_cache
            if search_query.lower() in post.title.lower() or search_query.lower() in post.body.lower()
               or any(search_query.lower() in comment.body.lower() for comment in post.comments)
               or any(search_query.lower() in comment.name.lower() for comment in post.comments)
        ]

    def sort_by_last_used(self) -> List[PostRecord]:
        return sorted(self._posts_cache, key=lambda post: post.last_used, reverse=True)

    def cleanup_old_records(self, threshold_seconds: int):
        now = datetime.utcnow()
        self._posts_cache = [
            post for post in self._posts_cache
            if (now - post.last_used).total_seconds() <= threshold_seconds
        ]

    def get_all_posts_as_json(self) -> List[dict]:
        # Konwersja wszystkich postów do formatu JSON (lista słowników)
        return [post.__dict__ for post in self._posts_cache]


    def get_all_comments_as_json(self):
        return [comment.__dict__ for comment in self._comments_cache]