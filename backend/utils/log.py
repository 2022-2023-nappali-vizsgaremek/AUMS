# local imports
import logging

log = logging.getLogger(__name__)

logging.basicConfig(
    filemode="w", filename="app.log",
    datefmt="%H:%M:%S", level=logging.DEBUG,
    format="(%(asctime)s) %(levelname)s: %(message)s")