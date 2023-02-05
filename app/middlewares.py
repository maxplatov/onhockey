import string
import time
import random

from loguru import logger

from starlette.requests import Request
from starlette.responses import JSONResponse


async def response_observer(request: Request, call_next):
    r_mark = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"mark={r_mark} start request {request.method} path={request.url.path}")
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as e:
        logger.exception(f"Request {r_mark} fail. Path {request.url.path}. Error {e}")
        return JSONResponse(status_code=500, content={"message": str(e)})
    else:
        process_time = (time.time() - start_time) * 1000
        process_time = '{0:.2f}'.format(process_time)
        logger.info(
            f"mark={r_mark} completed_in={process_time}ms status_code={response.status_code}"
        )

        return response
