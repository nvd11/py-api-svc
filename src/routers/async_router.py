
import src.configs.config
from loguru import logger
import time
import asyncio
from datetime import datetime
from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/async/test/{item_id}")
async def async_test(item_id: int,request: Request):
    time_start = time.time()
    await asyncio.sleep(2)
    time_end = time.time()

    # 格式化时间，并截取前3位微秒以得到毫秒
    start_str = datetime.fromtimestamp(time_start).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    end_str = datetime.fromtimestamp(time_end).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    infostr = f"item id {item_id} started at: {start_str}, ended at: {end_str}, time costed:{time_end - time_start:.2f} seconds"
    logger.info(infostr)
    return {"message": "This is an async test endpoint.", "info": infostr}
