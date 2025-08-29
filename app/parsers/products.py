from bs4 import BeautifulSoup as bs
from fastapi import HTTPException

from app.schemas.products import OfferSchema
from app.utils.requests_handler import RequestsHandler
from app.parsers.selectors import product_selectors


class ProductParser(RequestsHandler):
    async def collect_data(
        self,
        url: str,
        timeout_limit: int = None,
        count_limit: int = None,
    ):
        offers = []
        response = await self.fetch_data(url=url, timeout_limit=timeout_limit)
        
        soup = bs(response, "lxml")

        product_offers_container = soup.select_one(product_selectors.PRODUCT_OFFERS_CONTAINER_SEL)
        if not product_offers_container:
            raise HTTPException(status_code=404, detail="Not found Product offers container")
        
        offer_blocks = product_offers_container.select(product_selectors.OFFER_BLOCK_SEL)
        if not offer_blocks:
            raise HTTPException(status_code=404, detail="Not found id Offer blocks")
        
        for offer in offer_blocks:
            try:
                href = offer.select_one(product_selectors.SHOP_TITLE_SEL)['href']
                offer_url = href if 'https://hotline.ua' in href else f'https://hotline.ua{href}'

                original_url = await self.fetch_redirect_url(offer_url)
                print(original_url)

                product_title = offer.select_one(product_selectors.PRODUCT_TITLE_SEL).get_text(strip=True)
                shop_title = offer.select_one(product_selectors.SHOP_TITLE_SEL).get_text(strip=True)

                price = offer.select_one(product_selectors.PRICE_SEL)
                if price:
                    price = int(''.join(filter(str.isdigit, price.get_text())))
                else:
                    price = None
                
                is_used = offer.select_one(product_selectors.IS_USED_SEL)
                if is_used:
                    is_used = True
                else:
                    is_used = False


                offer_data = OfferSchema(
                    url=offer_url,
                    original_url=original_url,
                    title=product_title,
                    shop=shop_title,
                    price=price,
                    is_used=is_used
                )
                offers.append(offer_data)

                if count_limit and len(offers) >= count_limit:
                    break
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Unexpected error: {str(e)}"
                )
        return offers

        

product_parser = ProductParser()