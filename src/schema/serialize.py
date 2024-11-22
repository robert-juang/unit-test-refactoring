from config import logger 
from typing import List

def serialize_output(request_id: str, prediction: List):
    """Serializes the output of the model"""
    schema = {
        "request_id": request_id,
        "data": []}
    data_schema = {'prediction': prepare_content(prediction)} 
    schema["data"].append(data_schema)

    logger.info("Schema: " + str(schema))
    return schema

def prepare_content(prediction):
    """Returns List of dict for serialized output"""
    if not prediction: 
        return [] 
    elif isinstance(prediction, list):
        return prediction

    return [prediction]