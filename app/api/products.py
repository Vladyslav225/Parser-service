from fastapi import APIRouter, Query

from app.schemas.products import ProductResponseSchema, OfferSchema
from app.parsers.products import product_parser


product_router = APIRouter(
    prefix="/product",
    tags=["Products"]
)


@product_router.get(
    "/offers",
    response_model=ProductResponseSchema
)
async def view_product_offers(
    url: str = Query(..., description="The URL of the product to fetch offers for"),
    timeout_limit: int = Query(None, description="Timeout limit for fetching offers in seconds"),
    count_limit: int = Query(None, description="Maximum number of offers to return"),
    # TODO: Add sorting functionality after set up the functionality in parser prices
    # sort: bool = Query(False, description="Whether to sort offers by price")
):
    
    offers = await product_parser.collect_data(
        url=url,
        timeout_limit=timeout_limit,
        count_limit=count_limit,
    )
    
    return ProductResponseSchema(
        url=url,
        offers=[OfferSchema(**offer) for offer in offers]
    )