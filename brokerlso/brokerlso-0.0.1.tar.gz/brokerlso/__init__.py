import logging
import sys

FORMAT = "%(asctime)s : %(pathname)s : %(name)s : %(module)s : %(funcName)s : %(lineno)d : %(levelname)s : %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("brokerlso")
