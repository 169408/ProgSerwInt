import os
from datetime import datetime

if os.name == 'nt':  # 'nt' means Windows
    from ctypes import windll

import aiohttp

from typing import Iterable

from utils import consts
from domains.post import PostRecord
from domains.comment import PostComment
from repositories.ipost_respository import IPostRepository

class PostRepository:

    async def get_all_post_params(self) -> Iterable[PostRecord] | None:
        all_params = await self.get_all_posts()
        parsed_params = await self._parse_post_params(all_params)

        return parsed_params

    async def get_all_comment_params(self) -> Iterable[PostComment] | None:
        all_params = await self.get_all_comments()
        parsed_params = await self._parse_comment_params(all_params)

        return parsed_params

    async def _get_params(self, post_id: int) -> Iterable[dict] | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(consts.API_POST_URL.format(post_id=post_id)) as response:
                if response.status != 200:
                    return None

                return await response.json()

    async def _parse_post_params(self, params: Iterable[dict]) -> Iterable[PostRecord]:
        return [PostRecord(user_id=record.get("userId"), post_id=record.get("id"), title=record.get("title"), body=record.get("body"), last_used=datetime.utcnow(), comments=[]) for record in
                params[:]]

    async def _parse_comment_params(self, params: Iterable[dict]) -> Iterable[PostComment]:
        return [PostComment(post_id=record.get("postId"), comment_id=record.get("id"), name=record.get("name"), email=record.get("email"), body=record.get("body"), last_used=datetime.utcnow()) for record in
                params[:]]

    async def get_all_posts(self) -> Iterable[dict] | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(consts.API_POSTS_URL) as response:
                if response.status != 200:
                    return None

                return await response.json()

    async def get_all_comments(self) -> Iterable[dict] | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(consts.API_COMMENTS_URL) as response:
                if response.status != 200:
                    return None

                return await response.json()