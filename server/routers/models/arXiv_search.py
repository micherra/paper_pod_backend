from typing import Optional

from pydantic import BaseModel
from enum import Enum


# Create enum for sort_by
class SortBy(str, Enum):
    relevance = "relevance"
    lastUpdatedDate = "lastUpdatedDate"
    submittedDate = "submittedDate"


class SortOrder(str, Enum):
    ascending = "ascending"
    descending = "descending"


class ArXivSearch(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    abstract: Optional[str] = None
    category: Optional[str] = None
    start: Optional[int] = 0
    max_results: int = 10
    sort_by: SortBy = SortBy.relevance
    sort_order: SortOrder = SortOrder.descending
