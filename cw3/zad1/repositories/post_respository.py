import os
if os.name == 'nt':  # 'nt' means Windows
    from ctypes import windll

import aiohttp

from typing import Iterable

from utils import consts
from domains.post import PostRecord
from repositories.ipost_respository import IPostRepository

class PostRepository:

    async def get_all_post_params(self) -> Iterable[PostRecord] | None:
        all_params = await self.get_all_posts()
        parsed_params = await self._parse_post_params(all_params)

        return parsed_params

    async def _get_params(self, post_id: int) -> Iterable[dict] | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(consts.API_POST_URL.format(post_id=post_id)) as response:
                if response.status != 200:
                    return None

                return await response.json()

    async def _parse_post_params(self, params: Iterable[dict]) -> Iterable[PostRecord]:
        return [PostRecord(user_id=record.get("userId"), post_id=record.get("id"), title=record.get("title"), body=record.get("body")) for record in
                params[:]]


    async def get_all_posts(self) -> Iterable[dict] | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(consts.API_POSTS_URL) as response:
                if response.status != 200:
                    return None

                return await response.json()