from asyncio.log import logger
import logging
def logging_info(logger):
    logger= logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    f= logging.Formatter('%(asctime)s - %(name)s-%(lineno)d - %(levelname)s - %(message)s')
    fh = logging.FileHandler('logger.log')
    fh.setFormatter(f)
    logger.addHandler(fh)
    return logger