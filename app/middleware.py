import time
import logging
from fastapi import Request

logger = logging.getLogger("request-logger")

async def timing_middleware(request:Request,call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time()-start_time)*1000

    logger.info(
        "%s %s | status=%s | time=%.2fms",
        request.method,
        request.url.path,
        response.status_code,
        process_time
    )

    return response