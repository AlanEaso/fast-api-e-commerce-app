from fastapi import FastAPI
from .routers.api.v1 import router

app = FastAPI(title='E- Commerce App', version='1.0', description='E-Commerce app Made with FastApi and ❤️.')

app.include_router(router.api_v1_router, prefix='/api/v1')
