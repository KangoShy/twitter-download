import logging

from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

app = FastAPI()


def init_app():
    """
    初始化web服务
    :return:
    """
    router = APIRouter()

    @router.get("/health")
    def health() -> str:
        return "ok"

    app.include_router(router)


@app.exception_handler(ValueError)
async def generic_exception_handler(request, e):
    logging.exception("参数异常：" + getattr(e, 'message', repr(e)))
    return JSONResponse(status_code=500, content={"message": "参数异常：" + getattr(e, 'message', repr(e))})
