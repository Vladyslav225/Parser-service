from enum import Enum


class NewsSourceType(str, Enum):
    http = "http"
    browser = "browser"