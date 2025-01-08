from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.api.v1 import main
import logging
from app.middleware import error_handler_middleware

app = FastAPI(title='E- Commerce App', version='1.0', description='E-Commerce app Made with FastApi and ❤️.')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handling middleware
app.middleware("http")(error_handler_middleware)

app.include_router(main.api_v1_router, prefix='/api/v1')
