import sys, os 

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURR_DIR)) 

import uvicorn
from fastapi import FastAPI
from config import settings, ROOT_PATH, logger 
from routers import test_router

app = FastAPI(
    title="FastAPI",
    description="An example of FastAPI",
    version="0.0.1",
    contact={
        "name": "FastAPI",
    }, 
    root_path=ROOT_PATH
)

app.include_router(test_router.router)