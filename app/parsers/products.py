from bs4 import BeautifulSoup as bs
from fastapi import HTTPException

from app.schemas.products import OfferSchema
from app.handlers.requests_handler import RequestsHandler
from app.parsers.selectors import product_selectors
from app.utils.verify_element import verify_element


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
        verify_element(
            element=product_offers_container,
            message="Not found Product offers container",
            status_code=404
        )
        
        offer_blocks = product_offers_container.select(product_selectors.OFFER_BLOCK_SEL)
        verify_element(
            element=offer_blocks,
            message="Not found Offer blocks",
            status_code=404
        )
        
        for offer in offer_blocks:
            try:
                href = offer.select_one(product_selectors.SHOP_TITLE_SEL)['href']
                verify_element(
                    element=href,
                    message="Not found href in offer block",
                    status_code=404
                )
                offer_url = href if 'https://hotline.ua' in href else f'https://hotline.ua{href}'

                original_url = await self.fetch_redirect_url(offer_url)
                verify_element(
                    element=original_url,
                    message="Not found original url in offer block",
                    status_code=404
                )

                product_title = offer.select_one(product_selectors.PRODUCT_TITLE_SEL).get_text(strip=True)
                verify_element(
                    element=product_title,
                    message="Not found product title in offer block",
                    status_code=404
                )

                shop_title = offer.select_one(product_selectors.SHOP_TITLE_SEL).get_text(strip=True)
                verify_element(
                    element=shop_title,
                    message="Not found shop title in offer block",
                    status_code=404
                )

                # TODO: Fix price parsing
                # price = offer.select_one(product_selectors.PRICE_SEL)
                # if price:
                #     price = int(''.join(filter(str.isdigit, price.get_text())))
                # else:
                #     price = None
                
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
                    price=None,
                    is_used=is_used
                )
                offers.append(offer_data)

                if count_limit and len(offers) >= count_limit:
                    break
            except Exception as e:
                verify_element(
                    element=False,
                    message=f"Error parsing offer block: {str(e)}",
                    status_code=500
                )
        return offers

        

product_parser = ProductParser()