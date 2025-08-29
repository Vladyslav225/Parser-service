from fastapi import APIRouter, Query


news_router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@news_router.get("/source")
async def view_product_offers(
    url: str = Query(..., description="The URL of the product to fetch offers for"),
    until_date: str = Query(None, description="Fetch news until this date"),
    # TODO: client="http|browser"
    client: str = Query("http | browser", description="Client type to use for fetching the news")
):
    fake_offer = []

    return fake_offer