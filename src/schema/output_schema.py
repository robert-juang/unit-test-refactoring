from typing import Optional, Union, List, Dict  

# from langchain_core.pydantic_v1 import BaseModel, Field
from pydantic import BaseModel, Field
from pydantic import StrictStr, StrictInt, StrictFloat

class JsonSchema(BaseModel): 
    chain_of_thoughts: str = Field(description="Describe the steps you followed to write the code and the parts you focuysed")
    code: str = Field(description="The code you wrote") 

class CodeRefactoringPred(BaseModel): 
    code: str 
    explanation: str 

class Datum(BaseModel):
    prediction: List[CodeRefactoringPred]

class OutputSchema(BaseModel): 
    request_id: str 
    data: List[Datum]

class UnitTestSchema(BaseModel): 
    code_explanation: str 
    test_scenarios: str 
    unit_test: str 