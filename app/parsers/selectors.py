# INFO: Selectors for parsing products from hotline.ua
class ProductSelectors:
    def __init__(self):
        self.PRODUCT_OFFERS_CONTAINER_SEL = "div.default-layout__content-container div#tabs div#productOffersListContainer"
        self.OFFER_BLOCK_SEL = "div._3lPGH9nxRHNjZDXihhrb"
        self.SHOP_TITLE_SEL = "div._30YNRvfXIRxy4qSv8cQ3 a"
        self.PRODUCT_TITLE_SEL = "div._31oKPE8oY--GLfIUdlNp a[target='_blank'] div[data-tracking-id='goprice-6']"
        self.PRICE_SEL = "div._2zioiYHf7-sy7IvjJkL7 div._19Dv3k08LWZo1NYYYxWB"
        self.IS_USED_SEL = "div._31oKPE8oY--GLfIUdlNp div.m_b-5.text-gray.text-italic"


# INFO: Selectors for parsing news from different sources
class EpravdaNewsSelectors:
    def __init__(self):
        self.MAIN_SECTION_SEL = "div.main div.layout_wrapper"

        self.DATE_SEL = "div.section_page_date h2"
        self.NAV_BUTTON_SEL = "div.section_page_date a:nth-of-type(1)"

        self.ARTICLES_SECTIONS_SEL = "div.section_list_wrapper div.article_news"
        self.ARTICLE_LINKS_SEL = "div.article_title a"

        self.ARTICLE_MAIN_SEL = "div.section_news article.post_news"

        self.PRIMARY_ARTICLE_HEADER_SEL = "header.post_news_header"
        self.ALTERNATE_ARTICLE_HEADER_SEL = "header.post_header"

        self.PRIMARY_TITLE_SEL = "h1.post_news_title"
        self.ALTERNATE_TITLE_SEL = "h1.post_news_title"

        self.PRIMARY_AUTHOR_SEL = "span.post_news_author"
        self.ALTERNATE_AUTHOR_SEL = "div.post_author_name a"

        self.PRIMARY_PUBLISHED_DATE_SEL = "div.post_news_date"
        self.ALTERNATE_PUBLISHED_DATE_SEL = "div.post_service div.post_date"

        self.PRIMARY_CONTENT_BODY_SECTION_SEL = "div.post_news_body"

        self.PRIMARY_IMAGE_URLS_SEL = "div.post_news_photo img"
        self.ALTERNATE_IMAGE_URLS_SEL = "div.image-box.image-box_center img"
        self.CONTENT_BODY_SEL = "div.post_news_text"
        self.VIEWS_SEL = "div.post_views"
        self.COMMENTS_SEL = "iframe"
        self.LIKES_SEL = ""
        self.DISLIKES_SEL = ""
        self.VIDEO_SEL = ""

class PolitekaNewsSelectors:
    def __init__(self):
        self.MAIN_SECTION_SEL = ""

        self.DATE_SEL = ""
        self.NAV_BUTTON_SEL = ""

        self.ARTICLES_SECTION_SEL = ""
        self.ARTICLE_LINKS_SEL = ""

        self.ARTICLE_MAIN_SEL = ""

        self.ARTICLE_HEADER_SEL = ""
        self.TITLE_SEL = ""
        self.AUTHOR_SEL = ""
        self.PUBLISHED_DATE_SEL = ""

        self.CONTENT_BODY_SECTION_SEL = ""

        self.PRIMARY_IMAGE_URLS_SEL = ""
        self.ALTERNATE_IMAGE_URLS_SEL = ""
        self.CONTENT_BODY_SEL = ""
        self.VIEWS_SEL = ""
        self.COMMENTS_SEL = ""
        self.LIKES_SEL = ""
        self.DISLIKES_SEL = ""
        self.VIDEO_SEL = ""

class PravdaNewsSelectors:
    def __init__(self):
        self.MAIN_SECTION_SEL = "body.section_layout"

        self.DATE_SEL = "div.section_header.section_header_news div.section_header_date span"
        self.NAV_BUTTON_SEL = "div.section_header.section_header_news div.section_header_date a:nth-of-type(1)"

        self.ARTICLES_SECTIONS_SEL = "div.container_sub_news_list_wrapper.mode1 div.article_news_list"
        self.ARTICLE_LINKS_SEL = "div.article_content a"

        self.ARTICLE_MAIN_SEL = "div.container_sub_post_news article.post"

        self.ARTICLE_HEADER_SEL = "header.post_header"
        self.TITLE_SEL = "h1.post_title"
        self.AUTHOR_SEL = "div.post_time span.post_author"
        self.PUBLISHED_DATE_SEL = ""

        self.CONTENT_BODY_SECTION_SEL = ""

        self.PRIMARY_IMAGE_URLS_SEL = ""
        self.ALTERNATE_IMAGE_URLS_SEL = ""
        self.CONTENT_BODY_SEL = ""
        self.VIEWS_SEL = ""
        self.COMMENTS_SEL = ""
        self.LIKES_SEL = ""
        self.DISLIKES_SEL = ""
        self.VIDEO_SEL = ""


product_selectors = ProductSelectors()
epravda_selectors = EpravdaNewsSelectors()
politeka_selectors = PolitekaNewsSelectors()
pravda_selectors = PravdaNewsSelectors()