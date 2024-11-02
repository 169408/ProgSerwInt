from abc import ABC
from typing import List

class IPostService(ABC):
    async def load_data(self):
        pass

    async def filter_posts(self, search_query: str):
        pass


    async def get_all_posts_as_json(self) -> List[dict]:
        pass
