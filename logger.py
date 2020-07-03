import logging
import os


def setup_logger():
    logging.basicConfig(
        level="INFO",
        handlers=[
            logging.FileHandler(os.getenv("LOG_PATH")),
            logging.StreamHandler()],
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d %(identifier)s] %(message)s",
        datefmt="%H:%M:%S")

    logging.getLogger("discord").setLevel(logging.ERROR)


class ContextLogAdapter(logging.LoggerAdapter):
    def __init__(self, ctx=None):
        logger = logging.getLogger("tom_nook_bot")

        identifier = f"{ctx.guild}:{ctx.author}" if ctx else "Main"
        extra = {"identifier": identifier}

        super(ContextLogAdapter, self).__init__(logger, extra)
