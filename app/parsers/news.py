from app.parsers.news_workers.http_parser import http_parser
from app.parsers.selectors import epravda_selectors, politeka_selectors, pravda_selectors


class NewsParser:
    async def collect_data(
        self,
        source_url: str,
        until_date: str = None,
        client: str = "http"
    ):
        if "epravda.com.ua" in source_url:
            selectors = epravda_selectors
        elif "politeka.net" in source_url:
            selectors = politeka_selectors
        elif "pravda.com.ua" in source_url:
            selectors = pravda_selectors
        else:
            raise ValueError("Unsupported news source")
        
        if client == "http":
            return await http_parser.parser(
                source_url=source_url,
                until_date=until_date,
                selectors=selectors
            )
        
        # TODO: Implement browser parser using Playwright
        # if client == "browser":
        #     return await self.fetch_browser_data(
        #         url=url,
        #         until_date=until_date,
        #         selectors=selectors
        #     )
    
news_parser = NewsParser()