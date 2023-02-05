import uvicorn

from app.main import init_and_get_app
from app.config import CONFIG

if __name__ == "__main__":
    uvicorn.run(
        init_and_get_app(),
        host="0.0.0.0",
        port=CONFIG["app"]["port"],
    )
