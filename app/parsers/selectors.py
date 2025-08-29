class ProductSelectors:
    def __init__(self):
        self.PRODUCT_OFFERS_CONTAINER_SEL = "div.default-layout__content-container div#tabs div#productOffersListContainer"
        self.OFFER_BLOCK_SEL = "div[data-v-098ece02]._23pW3eU6gQev_150HTUX div._5fNQCyYWw6yrLHii4RFD"
        self.SHOP_TITLE_SEL = "div._30YNRvfXIRxy4qSv8cQ3 a"
        self.PRODUCT_TITLE_SEL = "div._31oKPE8oY--GLfIUdlNp a[target='_blank'] div[data-tracking-id='goprice-6']"
        self.PRICE_SEL = "div._2zioiYHf7-sy7IvjJkL7 div._19Dv3k08LWZo1NYYYxWB"
        self.IS_USED_SEL = "div._31oKPE8oY--GLfIUdlNp div.m_b-5.text-gray.text-italic"


class NewsSelectors:
    pass


product_selectors = ProductSelectors()
news_selectors = NewsSelectors()