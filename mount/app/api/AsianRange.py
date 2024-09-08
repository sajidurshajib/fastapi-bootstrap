from fastapi import APIRouter, Depends, Query
from app.dto.AsianRangeDTO import *
from app.usecases.AsianRange import *
from app.services.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.get("/asian-range-indicator-close/{market_type}/{ticker}", response_model=ResponseDTO)
async def asian_range_indicator_close(
    market_type: MarketType, ticker: str, timeframe: Timeframe = Query(Timeframe.MIN_15),
    start_date: str = Query(...), end_date: str = Query(...), start_time: str = Query(...),
    end_time: str = Query(...), overnight: Optional[bool] = Query(None), db: AsyncSession = Depends(get_db)
):
    service = AsianRangeIndicatorService(
        market_type=market_type, ticker=ticker, timeframe=timeframe,
        start_date=start_date, end_date=end_date, start_time=start_time,
        end_time=end_time, overnight=overnight, db=db
    )
    
    await service.fetch_data()
    
    if service.asian_session.empty or service.rest_of_day_session.empty or service.historical_data.empty:
        return {"error": "No historical data available"}
    
    return service.calculate_summary_and_detailed()