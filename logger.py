import logging

LOGGER_NAME = "tom_nook_bot"


def setup_logger():
    logging.basicConfig(
        level="INFO",
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d %(identifier)s] %(message)s",
        datefmt="%H:%M:%S")

    logging.getLogger("discord").setLevel(logging.ERROR)


class ContextLogAdapter(logging.LoggerAdapter):
    def __init__(self, ctx=None):
        logger = logging.getLogger(LOGGER_NAME)

        identifier = f"{ctx.guild}:{ctx.author}" if ctx else "setup"
        extra = {"identifier": identifier}

        super(ContextLogAdapter, self).__init__(logger, extra)
