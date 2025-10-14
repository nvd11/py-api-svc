
import src.configs.config
from loguru import logger
import time
from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/async/test/{item_id}")
async def async_test(item_id: int,request: Request):
    time_start = time.time()
    time.sleep(2)
    time_end = time.time()
    infostr = f"item id {item_id} started at:{time_start:.2f}, ended at:{time_end:.2f}, time costed:{time_end - time_start:.2f} seconds"
    logger.info(infostr)
    return {"message": "This is an async test endpoint.", "info": infostr}



