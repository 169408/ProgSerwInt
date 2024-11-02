import asyncio
from services.post_service import PostService

async def periodic_cleanup(service: PostService, interval: int, threshold: int):
    while True:
        await asyncio.sleep(interval)
        service.cleanup_old_records(threshold)