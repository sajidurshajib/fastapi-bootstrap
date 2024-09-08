from enum import Enum
from datetime import datetime, timedelta
from typing import List
from app.dto.AsianRangeDTO import *
import pandas as pd


class MarketType(str, Enum):
    STOCK = "stock"
    FOREX = "forex"
    CRYPTO = "crypto"

class Timeframe(str, Enum):
    MIN_15 = "15min"
    MIN_30 = "30min"
    HOUR_1 = "1h"


class AsianRangeIndicatorService:
    def __init__(self, market_type: MarketType, ticker: str, timeframe: Timeframe, start_date: str, end_date: str, start_time: str, end_time: str, overnight: Optional[bool], db: AsyncSession):
        self.market_type = market_type
        self.ticker = ticker
        self.timeframe = timeframe
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.overnight = overnight
        self.db = db

    async def fetch_data(self):
        self.asian_session, self.rest_of_day_session = await fetch_historical_intraday_data_multi_session(
            self.db, market_type=self.market_type, timeframe=self.timeframe, ticker=self.ticker,
            start_date=self.start_date, end_date=self.end_date, start_time=self.start_time, end_time=self.end_time,
            overnight=self.overnight
        )
        self.historical_data = await fetch_historical_data(
            self.db, market_type=self.market_type, ticker=self.ticker, start_date=self.start_date, end_date=self.end_date
        )

    def calculate_summary_and_detailed(self):
        summary = Summary()
        detailed_rows = []

        for _, asian_data in self.asian_session.iterrows():
            date = asian_data['date']
            if date in self.rest_of_day_session['grouped_date'].values:
                asian_high = asian_data['high']
                asian_low = asian_data['low']
                rest_day_data = self.rest_of_day_session[self.rest_of_day_session['grouped_date'] == date]
                
                for _, row in rest_day_data.iterrows():
                    close_price = self.get_closing_price(date)
                    if row['close'] > asian_high:
                        summary.update_closed_above(close_price, asian_high, date, detailed_rows)
                        break
                    elif row['close'] < asian_low:
                        summary.update_closed_below(close_price, asian_low, date, detailed_rows)
                        break

        return summary.generate_summary_report(self.historical_data, detailed_rows)

    def get_closing_price(self, date: datetime):
        try:
            return self.historical_data.loc[self.historical_data['date'] == date, 'close'].iloc[0]
        except IndexError:
            next_day = date + timedelta(days=1)
            close_price = self.historical_data.loc[self.historical_data['date'] == next_day, 'close']
            return close_price.iloc[0] if not close_price.empty else None


class Summary:
    def __init__(self):
        self.data = {
            'closedAbove': {'totalDays': 0, 'closedAboveHigh': 0, 'closedBelowHigh': 0},
            'closedBelow': {'totalDays': 0, 'closedAboveLow': 0, 'closedBelowLow': 0}
        }

    def update_closed_above(self, close_price, asian_high, date, detailed_rows):
        self.data['closedAbove']['totalDays'] += 1
        if close_price >= asian_high:
            self.data['closedAbove']['closedAboveHigh'] += 1
            self.add_detailed_row(date, "closed above AR", "closed above AR high", detailed_rows)
        else:
            self.data['closedAbove']['closedBelowHigh'] += 1
            self.add_detailed_row(date, "closed above AR", "closed below AR high", detailed_rows)

    def update_closed_below(self, close_price, asian_low, date, detailed_rows):
        self.data['closedBelow']['totalDays'] += 1
        if close_price >= asian_low:
            self.data['closedBelow']['closedAboveLow'] += 1
            self.add_detailed_row(date, "closed below AR", "closed above AR low", detailed_rows)
        else:
            self.data['closedBelow']['closedBelowLow'] += 1
            self.add_detailed_row(date, "closed below AR", "closed below AR low", detailed_rows)

    @staticmethod
    def add_detailed_row(date, range_closing_area, breakout_closing, detailed_rows):
        detailed_rows.append({
            "date": date.strftime('%Y-%m-%d'),
            "asian range closing area": range_closing_area,
            "breakout closing": breakout_closing,
            "details": "view price chart"
        })

    def generate_summary_report(self, historical_data: pd.DataFrame, detailed_rows: List[dict]):
        closed_above = self.data['closedAbove']['totalDays']
        closed_above_closed_high = self.data['closedAbove']['closedAboveHigh']
        closed_above_closed_low = self.data['closedAbove']['closedBelowHigh']
        closed_below = self.data['closedBelow']['totalDays']
        closed_below_closed_high = self.data['closedBelow']['closedAboveLow']
        closed_below_closed_low = self.data['closedBelow']['closedBelowLow']

        total_days = closed_above + closed_below
        closed_above_percentage = round((closed_above / total_days) * 100) if total_days > 0 else 0
        closed_above_green_percentage = round(closed_above_closed_high / closed_above * 100) if closed_above > 0 else 0
        closed_below_percentage = round((closed_below / total_days) * 100) if total_days > 0 else 0
        closed_below_green_percentage = round(closed_below_closed_high / closed_below * 100) if closed_below > 0 else 0

        return ResponseDTO(
            startDate=historical_data['date'].iloc[0].strftime('%Y-%m-%d'),
            endDate=historical_data['date'].iloc[-1].strftime('%Y-%m-%d'),
            summary=[
                SummaryDTO(category='first close above AR', frequency=closed_above, percentage=closed_above_percentage),
                SummaryDTO(category='first close above AR day closed above AR high', frequency=closed_above_closed_high, percentage=closed_above_green_percentage),
                SummaryDTO(category='first close above AR day closed below AR high', frequency=closed_above_closed_low, percentage=0 if closed_above_closed_low == 0 else 100 - closed_above_green_percentage),
                SummaryDTO(category='first close below AR', frequency=closed_below, percentage=closed_below_percentage),
                SummaryDTO(category='first close below AR day closed above AR low', frequency=closed_below_closed_high, percentage=closed_below_green_percentage),
                SummaryDTO(category='first close below AR day closed below AR low', frequency=closed_below_closed_low, percentage=0 if closed_below_closed_low == 0 else 100 - closed_below_green_percentage),
            ],
            detailed=detailed_rows
        )