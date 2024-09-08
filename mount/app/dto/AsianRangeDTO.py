from pydantic import BaseModel
from typing import List, Optional

class SessionDataDTO(BaseModel):
    date: str
    high: float
    low: float

class SummaryDTO(BaseModel):
    category: str
    frequency: int
    percentage: int

class DetailedDTO(BaseModel):
    date: str
    asian_range_closing_area: str
    breakout_closing: str
    details: str

class ResponseDTO(BaseModel):
    startDate: str
    endDate: str
    summary: List[SummaryDTO]
    detailed: List[DetailedDTO]