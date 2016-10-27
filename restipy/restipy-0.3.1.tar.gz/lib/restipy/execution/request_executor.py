import requests, logging

from requests import Request, Session

logger = logging.getLogger(__name__)

class RecipeRequestExecutor:
    def execute(self, recipe):
        logger.debug('Initiating request for recipe. %s', recipe);

        request = Request(**recipe['request'])
        session = Session()

        response = session.send(request.prepare())
        return response
