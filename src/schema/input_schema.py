from typing import Optional, Union, List, Dict  

from pydantic import BaseModel
from pydantic import StrictStr, StrictInt, StrictFloat

class InputKeys(BaseModel):
    username: StrictStr
    session_id: Optional[StrictStr] 
    prompt: str 
    mode: StrictStr