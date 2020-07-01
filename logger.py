import logging


def setup_logger():
    logging.basicConfig(
        level="INFO",
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%H:%M:%S")

    logging.getLogger("discord").setLevel(logging.ERROR)

    return logging.getLogger(__name__)


class ContextLogAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        super(ContextLogAdapter, self).__init__(logger, extra or {})


# def get_log_adapter(logger, ctx):
#     extra = {"identifier": "Setup"}
#     if ctx:
#         extra["identifier"] = f"{ctx.guild}{ctx.author}"

#     return logging.LoggerAdapter(logger, extra)
