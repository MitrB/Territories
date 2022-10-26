import logging

def config_logging():
    logging.basicConfig(level=logging.DEBUG, filename="debug.log", filemode="w")

    # disable/enable logging
    # logging.disable(logging.DEBUG)
    # logging.disable(logging.INFO)