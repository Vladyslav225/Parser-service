from fastapi import APIRouter, Query
from datetime import date

from app.enums.news import NewsSourceType
from app.schemas.news import NewsResponseSchema
from app.parsers.news import news_parser


news_router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@news_router.get(
    "/source",
    response_model=NewsResponseSchema
)
async def view_product_offers(
    source_url: str = Query(..., description="The URL of the product to fetch offers for"),
    until_date: date = Query(default=date.today(), description="Fetch news until this date. Format: YYYY-MM-DD"),
    client: NewsSourceType = Query(..., description="The client to use for fetching news using http or browser method")
):
    news_data = await news_parser.collect_data(
        source_url=source_url,
        until_date=until_date,
        client=client
    )

    return NewsResponseSchema(
        source=source_url,
        items=news_data
    )