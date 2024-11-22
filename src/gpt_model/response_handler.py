import aiohttp 
import json 
import re 
import requests
import uuid 

from config import logger, settings
from errors import UnknownGPTError

from collections import defaultdict
from fastapi import status 
from typing import List, Dict, Tuple, Any 
import numpy as np

class GPTResponseHandler(): 
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.gpt_version = settings.GPT_VERSION

    def _get_payload(self, req_id, user_message, system_message=None): 
        messages = [{"role": "user", "content": user_message}]

        if system_message: 
            messages.insert(0, {"role": "system", "content": system_message})

        payload = {
            'session_id': req_id, 
            "messages": messages, 
            "n": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "temperature": 0, 
            "top_p": 1, 
            "stop": None,
        }



        return payload
    
    def fix_gpt_response(self, input_response: str): 
        return input_response
    
    def _succeed_response(self, input_response: str):
        response = self.fix_gpt_response(input_response)

        response_content = response["choices"][0]["message"]["content"]

        json_response = response_content.replace('<json>', '').replace('</json>', '') 

        try: 
            json_response = json.loads(json_response) 
        except json.JSONDecodeError as e:
            json_response = self._fix_json_error(json_response)
            json_response = json.loads(json_response)
        
        return response, json_response 
    
    @retry_call(exception=(GPTExtractionError), max_retries=settings.MAX_RETRIES)
    async def gpt_call(self,
                       url: str, 
                       user_message: str, 
                       system_message: str, 
                       req_id: str=""): 
        url = url.replace("__req_id__", req_id) 
        payload = self._get_payload(req_id, user_message, system_message)

        logger.info(f"Requesting GPT with payload: {payload}")

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=15, ssl=False)) as session:
            async with session.post(url, headers=self._get_headers(), data = json.dumps(payload), verify_ssl=False) as response:
                status_code = response.status
                response_text = await response.text()

                response = await response.json()
                logger.info(f"Response received from GPT: {response}")
                
                if status_code == 200:
                    response_json = await response.json() 
                    response_data, json_response = self._succeed_response(response_json)

                    return {
                        "status_code": status_code, 
                        "response_text": response_text,
                        "response_data": response_data, 
                        "json_response": json_response
                    } 
                
                elif status_code == 429: 
                    logger.error(f"Rate limit error: {response_text}")
                    raise GPTRateLimitError(response_text) 
                
