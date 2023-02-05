import sys
import alembic.command
import alembic.config
from fastapi import FastAPI
from loguru import logger

from app.orm.engine import create_db_and_tables
from app.routers import setup_routes
from app.middlewares import response_observer
from app.config import DSN


def setup_middlewares(fastapi_app: FastAPI):
    fastapi_app.middleware("http")(response_observer)


async def on_startup():
    conf = alembic.config.Config("alembic.ini")
    conf.attributes["configure_logger"] = False
    conf.set_section_option(conf.config_ini_section, "sqlalchemy.url", DSN)
    alembic.command.upgrade(conf, "head")
    await create_db_and_tables()

    logger.info("On startup end")


def init_and_get_app():
    # off stack trace with vars, because may leak sensitive data in prod
    logger.remove()
    logger.add(sys.stderr, diagnose=False)

    fastapi_app = FastAPI(
        title="Onhockey",
    )
    setup_routes(fastapi_app)
    setup_middlewares(fastapi_app)

    fastapi_app.add_event_handler("startup", on_startup)
    return fastapi_app
