from typing import Annotated
from app.core.config import settings
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from fastapi import Header, HTTPException

async def get_product_header(x_token: Annotated[str, Header()]):
    if x_token != settings.PRODUCT_TOKEN:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    
async def get_order_header(x_token: Annotated[str, Header()]):
    if x_token != settings.ORDER_TOKEN:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
