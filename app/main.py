from fastapi import FastAPI
from app.api.products import product_router
from app.api.news import news_router

app = FastAPI(
    title="API Parser",
)

app.include_router(product_router)
app.include_router(news_router)