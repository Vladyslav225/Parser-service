from pydantic import BaseModel, model_validator
from typing import Optional, List


class ArticleDataSchema(BaseModel):
    title: Optional[str] = None
    content_body: Optional[str] = None
    image_urls: List[str] = []
    published_at: Optional[str] = None
    author: Optional[str] = None
    views: Optional[int] = None
    comments: List[str] = []
    likes: Optional[int] = None
    dislikes: Optional[int] = None
    video_url: Optional[str] = None


class NewsItemsSchema(BaseModel):
    source: Optional[str] = None
    url: Optional[str] = None
    article_data: Optional[ArticleDataSchema] = None
    

class NewsResponseSchema(BaseModel):
    source: Optional[str] = None
    items: List[NewsItemsSchema] = []