from abc import ABC
from typing import Iterable

from domains.post import PostRecord


class IPostRepository(ABC):

    async def get_all_post_params(self, sensor_id: int) -> Iterable[PostRecord] | None:
        pass