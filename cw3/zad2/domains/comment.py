from dataclasses import dataclass
from datetime import datetime


@dataclass
class PostComment:
    post_id: int
    comment_id: int
    name: str
    email: str
    body: str
    last_used: datetime

