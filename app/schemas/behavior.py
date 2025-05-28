from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class BehaviorLog(BaseModel):
    user_id: str
    timestamp: datetime
    commands: List[str]
    command_intervals: List[float]
    file_accessed: List[str]
    keystroke_intervals: List[float]
    id: Optional[str] = Field(None, alias="_id")
