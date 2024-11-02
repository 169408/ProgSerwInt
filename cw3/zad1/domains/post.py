from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class PostRecord:
    user_id: int
    post_id: int
    title: str
    body: str