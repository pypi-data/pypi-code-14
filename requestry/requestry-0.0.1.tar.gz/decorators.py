import logging
import time

logger = logger = logging.getLogger(__name__)


class RequestRetrial(object):
    """
        Decorator for adding a retrial mechanism to the requests made
    """
    
    def __init__(self, retry_count):
        """
        initializing the retry count here
        Args:
            retry_count: number of times the function has to be retried
        """
        self.retry_count = retry_count
    
    def __call__(self, func, *args):
        """
        overriding the function call and adding a retrial logic here.
        Args:
            func: the function here

        Returns: the response after the retrial mechanism

        """
        
        def wrapped_func(*args, **kwargs):
            
            count = 0
            while True:
                response = func(*args, **kwargs)
                if response.status_code == 200:
                    return response
                elif response.status_code >= 500:
                    if count == self.retry_count:
                        return response
                    else:
                        time.sleep(pow(2, count))
                    count += 1
                    continue
                else:
                    return response
        
        return wrapped_func
