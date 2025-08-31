from bs4 import BeautifulSoup as bs

import dateparser
from datetime import datetime
import zoneinfo
import asyncio
from urllib.parse import urljoin

from app.schemas.news import NewsItemsSchema, ArticleDataSchema
from app.handlers.requests_handler import RequestsHandler
from app.utils.verify_element import find_one_element, find_all_elements


class HttpParser(RequestsHandler):
    async def get_html(self, url: str):
        response = await self.fetch_data(url=url)
        return bs(response, "lxml")
    
    async def convert_date(self, date_str: str):
        return dateparser.parse(date_str).date()
    
    async def formating_date(self, date: str, published_date: str = None):
        full_published_date = datetime.fromisoformat(f'{date}T{published_date if published_date else "00:00:00"}')
        time_zone = zoneinfo.ZoneInfo("Europe/Kiev")
        full_published_date = full_published_date.replace(tzinfo=time_zone)
        return full_published_date.isoformat()
    
    async def collect_article_data(
            self,
            articles_on_page: list,
            selectors: object,
            date: str
    ):
        results = []

        for article_url in articles_on_page:
            print(f"Processing article: {article_url}")
            try:
                soup = await self.get_html(article_url)

                main_section = await find_one_element(
                    parent_element=soup,
                    selector=selectors.ARTICLE_MAIN_SEL,
                    error_message="Not found main section",
                    status_code=404
                )

                header = await find_one_element(
                    parent_element=main_section,
                    selector=selectors.PRIMARY_ARTICLE_HEADER_SEL,
                    error_message="Not found header",
                    status_code=404
                )
                if header is None:
                    header = await find_one_element(
                        parent_element=main_section,
                        selector=selectors.ALTERNATE_ARTICLE_HEADER_SEL,
                        error_message="Not found alternate header",
                        status_code=404
                    )

                title = await find_one_element(
                    parent_element=header,
                    selector=selectors.PRIMARY_TITLE_SEL,
                    error_message="Not found title",
                    status_code=404
                )
                if title is None:
                    title = await find_one_element(
                        parent_element=header,
                        selector=selectors.ALTERNATE_TITLE_SEL,
                        error_message="Not found alternate title",
                        status_code=404
                    )

                author = await find_one_element(
                    parent_element=header,
                    selector=selectors.PRIMARY_AUTHOR_SEL,
                    error_message="Not found author",
                    status_code=404
                )
                if author is None:
                    author = await find_one_element(
                        parent_element=header,
                        selector=selectors.ALTERNATE_AUTHOR_SEL,
                        error_message="Not found alternate author",
                        status_code=404
                    )

                published_date = None
                if author is None:
                    published_date = await find_one_element(
                        parent_element=header,
                        selector=selectors.PRIMARY_PUBLISHED_DATE_SEL,
                        error_message="Not found published date",
                        status_code=404
                    )
                    if published_date is None:
                        published_date = await find_one_element(
                            parent_element=header,
                            selector=selectors.ALTERNATE_PUBLISHED_DATE_SEL,
                            error_message="Not found alternate published date",
                            status_code=404
                        )
                    date_text = published_date.get_text(strip=True) if published_date else None
                    published_date = date_text.split(',')[-1].strip() if date_text else None

                if author is not None:
                    published_date = author.next_sibling
                    published_date = published_date.split(',')[-1].strip() if published_date else None
            
                published_at = await self.formating_date(date=date, published_date=published_date)

                content_body_section = await find_one_element(
                    parent_element=main_section,
                    selector=selectors.PRIMARY_CONTENT_BODY_SECTION_SEL,
                    error_message="Not found content body",
                    status_code=404
                )

                images = await find_all_elements(
                    parent_element=content_body_section,
                    selector=selectors.PRIMARY_IMAGE_URLS_SEL,
                    error_message="Not found images",
                    status_code=404
                )
                if not images:
                    images = await find_all_elements(
                        parent_element=content_body_section,
                        selector=selectors.ALTERNATE_IMAGE_URLS_SEL,
                        error_message="Not found alternate images",
                        status_code=404
                    )

                images_urls = []
                for image in images:
                    image_url = image.get("src")
                    images_urls.append(image_url)

                content_body = await find_one_element(
                    parent_element=content_body_section,
                    selector=selectors.CONTENT_BODY_SEL,
                    error_message="Not found content body text",
                    status_code=404
                )

                views = await find_one_element(
                    parent_element=main_section,
                    selector=selectors.VIEWS_SEL,
                    error_message="Not found views",
                    status_code=404
                )

                comments = await find_one_element(
                    parent_element=main_section,
                    selector=selectors.COMMENTS_SEL,
                    error_message="Not found comments",
                    status_code=404
                )

                await asyncio.sleep(1)

                results.append(
                    ArticleDataSchema(
                        title=title.get_text(strip=True) if title else None,
                        content_body=content_body.get_text(strip=True) if content_body else None,
                        image_urls=images_urls if images_urls else [],
                        published_at=published_at if published_at else None,
                        author= author.get_text(strip=True) if author else None,
                        views=int(views.get_text(strip=True)) if views and views.get_text(strip=True).isdigit() else None,
                        comments=comments if comments else [],
                        likes=0,
                        dislikes=0,
                        video_url=None
                    )
                )
            except Exception as e:
                print(f"Error processing article {article_url}: {e}")
                break

        return results


    async def parser(
        self,
        selectors: object,
        source_url: str,
        until_date: str = None
    ):
        items = []
        article_data = []

        current_url = source_url

        while True:
            try:
                soup = await self.get_html(url=current_url)

                main_section = await find_one_element(
                    parent_element=soup,
                    selector=selectors.MAIN_SECTION_SEL,
                    error_message="Not found main section",
                    status_code=404
                )

                date = await find_one_element(
                    parent_element=main_section,
                    selector=selectors.DATE_SEL,
                    error_message="Not found date element",
                    status_code=404
                )
                converted_date = await self.convert_date(date.get_text(strip=True))
                print(f"Current page date: {converted_date}")

                articles_on_page = []

                article_sections = await find_all_elements(
                    parent_element=main_section,
                    selector=selectors.ARTICLES_SECTIONS_SEL,
                    error_message="Not found articles section",
                    status_code=404
                )
                for article_section in article_sections:
                    article_link = await find_one_element(
                        parent_element=article_section,
                        selector=selectors.ARTICLE_LINKS_SEL,
                        error_message="Not found article link",
                        status_code=404
                    )
                    article_url = urljoin(current_url, article_link.get("href"))
                    # print(f"Found article URL: {article_url}")
                    articles_on_page.append(article_url)
                
                article_data = await self.collect_article_data(
                    articles_on_page=articles_on_page,
                    selectors=selectors,
                    date=converted_date
                )

                for article_url, article_data in zip(articles_on_page, article_data):
                    items.append(
                        NewsItemsSchema(
                            source=source_url,
                            url=article_url,
                            article_data=article_data,
                        )
                    )

                nav_button = await find_one_element(
                    parent_element=main_section,
                    selector=selectors.NAV_BUTTON_SEL,
                    error_message="Not found navigation button",
                    status_code=404
                )
                next_page_url = urljoin(current_url, nav_button.get("href"))

                if until_date and converted_date <= until_date:
                    print(f"Reached the until_date: {until_date}. Stopping.")
                    break

                current_url = next_page_url

                await asyncio.sleep(1)

            except Exception as e:
                print(f"Error processing page {current_url}: {e}")
                break

        return items

        

http_parser = HttpParser()
