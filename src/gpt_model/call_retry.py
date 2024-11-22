import asyncio
import time 
import aiohttp 
import functools
from retry import retry 
from retry.api import retry_call 
from src.gpt_model.response_handler import GPTResponseHandler
import traceback 

import time
import inspect 
from config import logger, settings

from errors import UnknownGPTError

def retry_call(max_retries=settings.MAX_RETRIES):
    def decorator(api_call_fun): 
        @functools.wraps(api_call_fun)
        async def wrapper(*args, **kwargs):
            attempt = 1 
            while attempt <= max_retries: 
                try: 
                    return await api_call_fun(*args, **kwargs)
                except Exception as e:
                    logger.info(traceback.format_exc()) 
                    delay = settings.init_delay_seconds * 2 ** attempt 
                    attempt += 1
                    await asyncio.sleep(delay) 

                logger.error(f"Failed to call API after {max_retries} attempts")
                raise UnknownGPTError
        
        @functools.wraps(api_call_fun) 
        def sync_retry(*args, **kwargs):
            attempt = 1
            while attempt < max_retries: 
                try: 
                    return api_call_fun(*args, **kwargs)
                except Exception as e: 
                    logger.info(traceback.format_exc())
                    delay = settings.init_delay_seconds * 2 ** attempt 
                    attempt += 1
                    time.sleep(delay)
            logger.error(f"Failed to call API after {max_retries} attempts")
            raise UnknownGPTError

        if inspect.iscoroutinefunction(api_call_fun): 
            return wrapper 
        else: 
            return sync_retry   
    return decorator