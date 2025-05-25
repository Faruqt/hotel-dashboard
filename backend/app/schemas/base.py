# library imports
from pydantic import BaseModel
from typing import Optional


class PaginatedResponse(BaseModel):
    current_page: int
    page_size: int
    next_page: Optional[int] = None
    prev_page: Optional[int] = None
