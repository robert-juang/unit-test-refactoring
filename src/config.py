import os 
import logging 
from dotenv import load_dotenv, find_dotenv 

from pydantic_settings import baseSettings 

load_dotenv(override=True) 

ROOT_PATH = os.getenv("ROOT_PATH", None) 

class Settings(BaseSettings): 
    ENV: str = "sit"
    CONNECTING_STRING: str = "" 
    logger: logging.Logger = logger 

    EMBEDDINGS_API_KEY : str = "" 
    OPENAI_API_KEY: str = "" 
    OPENAI_API_BASE: str = "" 
    OPENAI_API_TYPE: str = "" 
    OPENAI_API_ENDPOINT: str = "" 
    LLM_MODEL_NAME: str = "" 
    GPT_USERNAME: str = "" 

    # ENV: os.getenv("ENV", "dev")
    # logger = logging.getLogger(__name__)
    # max_yt_api_calls = 100
    # model: str="gpt-4o-mini" 
    # youtube_developer_key: str=os.environ(youtube_developer_key, None) 

setting = Settings() 

if setting.ENV == "sit": 
    setting.OPENAI_API_BASE = os.getenv("OPENAI_API_BASE") 
    setting.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    setting.LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")

logger = setting.logger 

