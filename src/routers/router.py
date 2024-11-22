import os, sys
CURR_DIR = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(os.path.dirname(CURR_DIR))

import traceback 
import time 

from fastapi import APIRouter, status, HTTPException 
from errors import UnknownGPTError
from config import logger 

router = APIRouter() 

def on_load_event(): 
    transcript_module = TranscriptModule() 

@router.get('/test') 
def test(): 
    return {"message": "Hello world"} 

@api_router.post('/code-refactor') 
async def code_refactoring(inputs: input_schema.InputKeys()): 
                           
    logger.info("Request received.") 
    
    inputs = convert_to_dict(inputs,
                             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                             detail="Failed converting Inputs to dictionary", 
                             logger=logger) 

    try: 
        pred = llm_chain.call_gpt(inputs, mode="refactoring") 
        if isinstance(pred, str): 
            pred = restructure_output_format.postproc_json_format(pred, mode="refactoring") 
            pred = serialize_output(request_id=str(uuid.uuid4()), prediction=pred) 
            validate_output_schema(pred, OutputSchema) 

    except PostProcess as e: 
        error_message = f'{PostprocessError.code} {PostProcessError.description}' 

    except UnknownGPTError as e: 
        error_message = f'{PostprocessError.code} {PostProcessError.description}' 
        logger.error(traceback.format_exc() + error_message) 
        logger.info("Failed to convert response to JSON") 

    except Exception as e: 
        logger.error(e) 

    finally: 
        logger.info("Request completed") 

@api_router.post('/unit-test') 
async def code_refactoring(inputs: input_schema.InputKeys()): 
                           
    logger.info("Request received.") 
    
    inputs = convert_to_dict(inputs,
                             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                             detail="Failed converting Inputs to dictionary", 
                             logger=logger) 

    try: 
        pred = llm_chain.call_gpt(inputs, mode="refactoring") 
        if isinstance(pred, str): 
            pred = restructure_output_format.postproc_json_format(pred, mode="refactoring") 
            pred = serialize_output(request_id=str(uuid.uuid4()), prediction=pred) 
            validate_output_schema(pred, OutputSchema) 

    except PostProcess as e: 
        error_message = f'{PostprocessError.code} {PostProcessError.description}' 

    except UnknownGPTError as e: 
        error_message = f'{PostprocessError.code} {PostProcessError.description}' 
        logger.error(traceback.format_exc() + error_message) 
        logger.info("Failed to convert response to JSON") 

    except Exception as e: 
        logger.error(e) 

    finally: 
        logger.info("Request completed") 