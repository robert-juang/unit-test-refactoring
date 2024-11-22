import traceback 
from fastapi import HTTPException 
from pydantic import ValidationError 
from pydantic.error_wrappers import ErrorWrapper

def validate_input_schema(data, schema):
    try:
        schema(**data)
    except ValidationError as e:
        error_messages = [f"{error['loc']}: {error['msg']}" for error in e.errors()]
        raise HTTPException(status_code=400, detail=error_messages)

def validate_output_schema(data, schema):
    try:
        schema(**data)
    except ValidationError as e:
        error_messages = [f"{error['loc']}: {error['msg']}" for error in e.errors()]
        raise HTTPException(status_code=400, detail=error_messages)